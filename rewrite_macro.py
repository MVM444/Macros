# -*- coding: utf-8 -*-
from pathlib import Path
macro_path = Path('Macros-de-Freecad/Insertar_Dispositivo.FCMacro')
macro_text = """# -*- coding: utf-8 -*-
"""
Insertar_Dispositivo.FCMacro
Selector generico de dispositivo electrico usando electriccr.features.objeto_toma_uno.
"""

import json
import re
import sys
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui

try:
    from PySide2 import QtWidgets, QtCore
except Exception:
    from PySide import QtGui as QtWidgets  # type: ignore
    from PySide import QtCore  # type: ignore

MODE_CHOICES = [
    ("Ambos", "Ambos"),
    ("Solo 2D", "Solo2D"),
    ("Solo 3D", "Solo3D"),
]

_DEFAULT_LABEL_TEMPLATE = "{KeyRegistro}-{ConsecDoc:03d}"
_ALLOWED_2D_EXT = {".step", ".stp", ".dxf", ".iges", ".igs"}
_ALLOWED_3D_EXT = {".step", ".stp", ".iges", ".igs"}


def _log_info(message: str) -> None:
    App.Console.PrintMessage(f"[INSER][INFO] {message}\\n")


def _log_warn(message: str) -> None:
    App.Console.PrintWarning(f"[INSER][WARN] {message}\\n")


def _log_error(message: str) -> None:
    App.Console.PrintError(f"[INSER][ERROR] {message}\\n")


def _user_appdata_dir() -> Path:
    try:
        return Path(App.getUserAppDataDir())
    except Exception:
        return Path.home() / "AppData" / "Roaming" / "FreeCAD"


def _user_macro_root() -> Path:
    base = _user_appdata_dir()
    for name in ("Macro", "Macros"):
        candidate = base / name
        if candidate.exists():
            return candidate
    return base / "Macro"


def _ensure_user_resource_tree() -> None:
    root = _user_macro_root()
    targets = [
        root / "Resources",
        root / "Resources" / "registry",
        root / "Resources" / "prototypes",
        root / "Resources" / "prototypes" / "2d",
        root / "Resources" / "prototypes" / "3d",
    ]
    created = []
    for path in targets:
        if path.exists():
            continue
        try:
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)
        except Exception as ex:
            _log_warn(f"No se pudo crear {path}: {ex}")
    if created:
        _log_info("Se crearon carpetas faltantes: " + ", ".join(str(p) for p in created))


def _candidate_registry_files() -> list[Path]:
    _ensure_user_resource_tree()
    candidates: list[Path] = []
    try:
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parents]:
            candidate = parent / "Resources" / "registry" / "registry_electric.json"
            if candidate.is_file():
                candidates.append(candidate)
                break
    except Exception:
        pass
    user_reg = _user_macro_root() / "Resources" / "registry" / "registry_electric.json"
    if user_reg.is_file():
        candidates.append(user_reg)
    return candidates


def _load_registry() -> tuple[str, dict, dict]:
    schema = "1.0.0"
    merged: dict[str, dict] = {}
    templates: dict[str, str] = {}
    for path in _candidate_registry_files():
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except Exception as ex:
            _log_warn(f"No se pudo leer {path}: {ex}")
            continue
        try:
            data = json.loads(raw)
        except Exception as ex:
            _log_warn(f"Registro ilegible en {path}: {ex}")
            continue
        if not isinstance(data, dict):
            continue
        if isinstance(data.get("types"), dict):
            for key, value in data["types"].items():
                if isinstance(value, dict):
                    merged[key] = value.copy()
        if "schema" in data:
            schema = str(data["schema"])
        if isinstance(data.get("labelTemplates"), dict):
            templates.update({str(k): str(v) for k, v in data["labelTemplates"].items()})
    if not merged:
        _log_warn("No se encontro registry_electric.json; usando tipo por defecto.")
        merged = {
            "Tomacorriente_120V": {
                "ifc": "IfcOutlet",
                "categoria": "Pared",
                "symbol2D": "Toma_2d.step",
                "model3D": "Toma_3d.step",
                "defaults": {"altura": 300, "modo": "Both", "orient2D_sigue_pared": True},
                "version": "1.0",
                "comentario": "Configuracion minima por defecto",
            }
        }
    return schema, merged, templates


def _mode_index_from_value(value: object) -> int:
    norm = str(value or "").strip().lower()
    for idx, (label, code) in enumerate(MODE_CHOICES):
        if norm == code.lower() or norm == label.lower():
            return idx
    if norm == "both":
        return 0
    if norm in {"2d", "solo2d", "solo 2d"}:
        return 1
    if norm in {"3d", "solo3d", "solo 3d"}:
        return 2
    return 0


def _sanitize_identifier(text: str) -> str:
    token = re.sub(r"[^0-9A-Za-z]+", "_", str(text or ""))
    token = token.strip("_")
    return token or "Proto"


def _proto_from_resource(resource: object, suffix: str) -> tuple[str, str | None]:
    name = str(resource or "").strip()
    if not name:
        return ("ProtoToma2D" if suffix == "2D" else "ProtoToma3D", None)
    stem = Path(name).stem.lower()
    if suffix == "2D" and stem in {"toma_2d", "toma_normal", "prototoma2d"}:
        return ("ProtoToma2D", name)
    if suffix == "3D" and stem in {"toma_3d", "tomacorriente-3d", "toma_normal", "prototoma3d"}:
        return ("ProtoToma3D", name)
    ext = Path(name).suffix.lower()
    if suffix == "2D" and ext not in _ALLOWED_2D_EXT:
        _log_warn(f"symbol2D '{name}' no es STEP/DXF soportado; se usara el prototipo por defecto")
        return ("ProtoToma2D", None)
    if suffix == "3D" and ext not in _ALLOWED_3D_EXT:
        _log_warn(f"model3D '{name}' no es STEP soportado; se usara el prototipo por defecto")
        return ("ProtoToma3D", None)
    label = f"Proto_{_sanitize_identifier(Path(name).stem)}_{suffix}"
    return (label, name)


def _logical_tipo(type_key: str, info: dict) -> str:
    explicit = (info or {}).get('tipo')
    if explicit:
        return str(explicit)
    key = (type_key or '').lower()
    if 'apagador' in key or 'switch' in key:
        return 'Apagador'
    if 'lumin' in key:
        return 'Luminaria'
    if 'sensor' in key:
        return 'Sensor'
    if 'rociador' in key:
        return 'Rociador'
    if 'altavoz' in key:
        return 'Altavoz'
    if 'camara' in key:
        return 'Camara'
    return 'Toma'


def _candidate_electriccr_dirs() -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()

    def register(path: Path) -> None:
        try:
            real = path.resolve()
        except Exception:
            real = path
        if real in seen:
            return
        seen.add(real)
        found.append(real)

    try:
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parents]:
            direct = parent / "ElectricCR"
            if (direct / "electriccr" / "features" / "objeto_toma_uno.py").is_file():
                register(direct)
    except Exception:
        pass

    user_root = _user_macro_root() / "ElectricCR"
    if (user_root / "electriccr" / "features" / "objeto_toma_uno.py").is_file():
        register(user_root)
    return found


def _ensure_electriccr_on_path() -> bool:
    import importlib

    def _try_import() -> bool:
        for name in ("ElectricCR", "electriccr"):
            try:
                importlib.import_module(name)
                return True
            except ImportError:
                continue
        return False

    if _try_import():
        return True

    for directory in _candidate_electriccr_dirs():
        for candidate in (directory.parent, directory):
            if candidate and candidate.exists():
                sdir = str(candidate)
                if sdir not in sys.path:
                    sys.path.insert(0, sdir)
        importlib.invalidate_caches()
        if _try_import():
            return True

    _log_error("No fue posible localizar la carpeta ElectricCR.")
    return False


def _next_elec_name(doc: App.Document) -> str:
    pattern = re.compile(r"^ELEC_(\\d{6})$")
    max_id = 0
    for obj in getattr(doc, 'Objects', []):
        match = pattern.match(obj.Name)
        if match:
            try:
                value = int(match.group(1))
            except Exception:
                continue
            if value > max_id:
                max_id = value
    return f"ELEC_{max_id + 1:06d}"


def _next_consecutive(doc: App.Document, key_registro: str) -> int:
    if not doc:
        return 1
    key = (key_registro or '').strip()
    counter = 0
    for obj in getattr(doc, 'Objects', []):
        if getattr(obj, 'KeyRegistro', '') == key:
            counter += 1
    return counter + 1


def _format_label(template: str, context: dict) -> str:
    try:
        return template.format(**context)
    except Exception as ex:
        _log_warn(f"Plantilla de etiqueta invalida '{template}': {ex}")
        return f"{context.get('KeyRegistro', 'Dispositivo')}-{context.get('ConsecDoc', 1):03d}"


def _ensure_label_template(templates: dict) -> str:
    if isinstance(templates, dict) and templates.get('default'):
        return str(templates['default'])
    return _DEFAULT_LABEL_TEMPLATE


class InsertarDispositivoDialog(QtWidgets.QDialog):
    def __init__(self, parent, schema: str, types: dict, templates: dict):
        super().__init__(parent)
        self.setWindowTitle("Insertar dispositivo electrico")
        self.setMinimumWidth(380)
        self.schema = schema
        self.types = types
        self.templates = templates or {}

        self.cmbTipo = QtWidgets.QComboBox()
        type_names = sorted(types.keys())
        if type_names:
            self.cmbTipo.addItems(type_names)
        else:
            self.cmbTipo.addItem("Tomacorriente_120V")

        self.spAltura = QtWidgets.QDoubleSpinBox()
        self.spAltura.setSuffix(" mm")
        self.spAltura.setRange(0, 10000)
        self.spAltura.setSingleStep(50.0)

        self.cmbModo = QtWidgets.QComboBox()
        for label, value in MODE_CHOICES:
            self.cmbModo.addItem(label, value)

        self.chkOrient2D = QtWidgets.QCheckBox("Alinear simbolo 2D con la pared")
        self.chkOrient2D.setChecked(True)

        self._apply_defaults_for(self.cmbTipo.currentText())
        self.cmbTipo.currentTextChanged.connect(self._on_tipo_changed)

        btn_ok = QtWidgets.QPushButton("Insertar")
        btn_cancel = QtWidgets.QPushButton("Cancelar")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        form = QtWidgets.QFormLayout()
        form.addRow("Tipo:", self.cmbTipo)
        form.addRow("Altura:", self.spAltura)
        form.addRow("Modo visual:", self.cmbModo)
        form.addRow("", self.chkOrient2D)

        btns = QtWidgets.QHBoxLayout()
        btns.addStretch(1)
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addLayout(btns)

    def selected_mode_code(self) -> str:
        data = self.cmbModo.currentData()
        if data:
            return data
        idx = max(0, self.cmbModo.currentIndex())
        return MODE_CHOICES[idx][1]

    def _apply_defaults_for(self, key: str) -> None:
        info = self.types.get(key, {}) or {}
        defaults = info.get("defaults", {}) or {}
        try:
            altura = float(defaults.get("altura", 300))
        except Exception:
            altura = 300.0
        self.spAltura.setValue(altura)
        modo = defaults.get("modo", MODE_CHOICES[0][1])
        self.cmbModo.setCurrentIndex(_mode_index_from_value(modo))
        orient = defaults.get("orient2D_sigue_pared", True)
        self.chkOrient2D.setChecked(bool(orient))

    def _on_tipo_changed(self, key: str) -> None:
        self._apply_defaults_for(key)


def _insert_dispositivo_from_dialog() -> None:
    schema, types, templates = _load_registry()
    dialog = InsertarDispositivoDialog(Gui.getMainWindow(), schema, types, templates)
    if dialog.exec_() != QtWidgets.QDialog.Accepted:
        return

    tipo_registro = dialog.cmbTipo.currentText().strip()
    altura = float(dialog.spAltura.value())
    modo = dialog.selected_mode_code()

    if not _ensure_electriccr_on_path():
        return

    try:
        from ElectricCR.electriccr.features.objeto_toma_uno import crear_toma_uno
    except ImportError:
        try:
            from electriccr.features.objeto_toma_uno import crear_toma_uno
        except ImportError as ex:
            _log_error(f"No se pudo importar objeto_toma_uno: {ex}")
            return

    doc = App.ActiveDocument or App.newDocument("Electrico")

    info = types.get(tipo_registro, {}) or {}
    tipo_logico = _logical_tipo(tipo_registro, info)
    key_registro = tipo_registro
    ifc_type = str(info.get("ifc", ""))
    categoria = str(info.get("categoria", "Pared")) or "Pared"

    proto2d_label, proto2d_src = _proto_from_resource(info.get("symbol2D"), "2D")
    proto3d_label, proto3d_src = _proto_from_resource(info.get("model3D"), "3D")
    grupo_inst = info.get("grupo", "Tomacorrientes")

    elec_name = _next_elec_name(doc)
    consec = _next_consecutive(doc, key_registro)
    label_template = _ensure_label_template(templates)
    context = {
        "Name": elec_name,
        "KeyRegistro": key_registro,
        "Tipo": tipo_logico,
        "ConsecDoc": consec,
    }
    etiqueta = _format_label(label_template, context)

    defaults = info.get("defaults", {}) or {}
    orient_default = str(defaults.get("orientacion", "Vertical")).title()
    if orient_default not in ("Vertical", "Horizontal", "Auto"):
        orient_default = "Vertical"
    if dialog.chkOrient2D.isChecked() and orient_default == "Vertical":
        orient_default = "Horizontal"

    objeto = crear_toma_uno(
        doc,
        name_hint=elec_name,
        instances_group_label=grupo_inst,
        label_2d=proto2d_label,
        label_3d=proto3d_label,
        proto2d_source=proto2d_src,
        proto3d_source=proto3d_src,
        name_prefix=f"{_sanitize_identifier(tipo_logico)}_",
        tipo=tipo_logico,
        categoria=categoria,
        key_registro=key_registro,
        ifc_type=ifc_type,
    )

    if objeto is None:
        _log_error("crear_toma_uno no devolvio una instancia valida.")
        return

    try:
        objeto.Label = etiqueta
    except Exception:
        pass

    try:
        objeto.ModoVisual = modo
    except Exception:
        _log_warn("No se pudo asignar ModoVisual al objeto.")

    try:
        objeto.AlturaRel = altura
    except Exception:
        _log_warn("No se pudo asignar AlturaRel al objeto.")

    try:
        objeto.KeyRegistro = key_registro
    except Exception:
        pass

    try:
        objeto.IfcType = ifc_type
    except Exception:
        pass

    try:
        objeto.Categoria = categoria
    except Exception:
        pass

    try:
        objeto.Orientacion
"""
macro_path.write_text(macro_text, encoding='utf-8')
