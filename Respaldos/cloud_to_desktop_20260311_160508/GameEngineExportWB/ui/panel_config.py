<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
"""Configuration TaskPanel for Game Engine Export WB.

Descripcion rapida: panel para ajustar rutas y preferencias globales.
Fecha y hora: 2025-10-13 19:00 UTC.
Instrucciones clave:
- Guardar preferencias usando ParamGet en Plugins/GameEngineExportWB.
- Permitir seleccionar rutas mediante dialogos con PySide.
- Mantener cadenas ASCII y mensajes con prefijo [GAMEEXPORT].
"""

import os
from pathlib import Path
from typing import Optional

from PySide import QtGui

from .output_defaults import compute_output_defaults, persist_output_settings

FreeCAD = __import__("FreeCAD")
FreeCADGui = __import__("FreeCADGui")

PARAM_GROUP = "User parameter:Plugins/GameEngineExportWB"


class ConfigTaskPanel:
    """TaskPanel to edit global configuration values."""

    def __init__(self):
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Opening configuration panel\n")
        self.params = FreeCAD.ParamGet(PARAM_GROUP)
        self.widget = QtGui.QWidget()
        self.widget.setWindowTitle("Game Engine Export - Configuracion")
        layout = QtGui.QVBoxLayout(self.widget)
        self.form = self.widget

        self.output_dir_line = QtGui.QLineEdit()
        self.base_name_line = QtGui.QLineEdit()
        self.launch_checkbox = QtGui.QCheckBox("Lanzar Castle Game Engine despues de exportar")
        self.cge_path_line = QtGui.QLineEdit()

        layout.addWidget(self._build_output_group())
        layout.addWidget(self._build_launch_group())

        layout.addStretch()
        self._load_values()

    def _build_output_group(self):
        group = QtGui.QGroupBox("Salida / Output")
        grid = QtGui.QGridLayout(group)

        grid.addWidget(QtGui.QLabel("Carpeta / Folder"), 0, 0)
        grid.addWidget(self.output_dir_line, 0, 1)
        btn_browse = QtGui.QPushButton("Examinar / Browse")
        btn_browse.clicked.connect(self._browse_output_dir)
        grid.addWidget(btn_browse, 0, 2)

        grid.addWidget(QtGui.QLabel("Nombre base / Base name"), 1, 0)
        grid.addWidget(self.base_name_line, 1, 1)
        self.base_name_line.setPlaceholderText("Default: etiqueta del documento")

        return group

    def _build_launch_group(self):
        group = QtGui.QGroupBox("Castle Engine")
        layout = QtGui.QVBoxLayout(group)

        self.launch_checkbox.setToolTip(
            "ES: Ejecuta Castle Engine tras exportar.\nEN: Launch Castle Engine after export."
        )
        layout.addWidget(self.launch_checkbox)

        path_layout = QtGui.QHBoxLayout()
        path_layout.addWidget(QtGui.QLabel("Ruta ejecutable / Executable path"))
        path_layout.addWidget(self.cge_path_line)
        btn_browse = QtGui.QPushButton("Examinar / Browse")
        btn_browse.clicked.connect(self._browse_cge_path)
        path_layout.addWidget(btn_browse)
        layout.addLayout(path_layout)

        return group

    def _load_values(self):
        doc_path = self._active_doc_path()
        output_dir, base_name, _ = compute_output_defaults(self.params, doc_path)
        self.output_dir_line.setText(output_dir)
        self.base_name_line.setText(base_name)
        self.launch_checkbox.setChecked(bool(self.params.GetBool("launch_cge", False)))
        self.cge_path_line.setText(self.params.GetString("cge_path", ""))

    def _active_doc_path(self) -> Optional[Path]:
        doc = FreeCAD.ActiveDocument
        if doc and getattr(doc, "FileName", ""):
            return Path(doc.FileName)
        return None

    def _browse_output_dir(self):
        start_dir = self.output_dir_line.text() or os.path.expanduser("~")
        selected = QtGui.QFileDialog.getExistingDirectory(
            self.widget, "Seleccionar carpeta de salida", start_dir
        )
        if selected:
            self.output_dir_line.setText(selected)

    def _browse_cge_path(self):
        start_path = self.cge_path_line.text() or os.path.expanduser("~")
        selected, _ = QtGui.QFileDialog.getOpenFileName(
            self.widget, "Seleccionar ejecutable de Castle Engine", start_path
        )
        if selected:
            self.cge_path_line.setText(selected)

    def _save_values(self):
        output_dir = self.output_dir_line.text().strip()
        base_name = self.base_name_line.text().strip()
        launch_cge = self.launch_checkbox.isChecked()
        cge_path = self.cge_path_line.text().strip()

        doc_path = self._active_doc_path()
        persist_output_settings(self.params, output_dir, base_name, doc_path)
        self.params.SetBool("launch_cge", bool(launch_cge))
        self.params.SetString("cge_path", cge_path)
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Configuration saved\n")

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

    def accept(self):
        self._save_values()
        FreeCADGui.Control.closeDialog()
        return True

    def reject(self):
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Configuration dialog cancelled\n")
        FreeCADGui.Control.closeDialog()
        return True


__all__ = ["ConfigTaskPanel"]
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
"""Configuration tab for Game Engine Export WB.

Descripcion rapida: controles de configuracion global y perfiles.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Mantener controles preparados para integracion con persistencia ParamGet.
- Evitar acentos y mantener comentarios claros.
- Proveer tooltips bilingues.
"""

from PySide import QtGui


def build_config_tab():
    """Return the configuration QWidget."""
    tab = QtGui.QWidget()
    layout = QtGui.QVBoxLayout(tab)

    info_label = QtGui.QLabel(
        "Salida y nombre base se ajustan en la pestana Escena para evitar duplicacion.\n"
        "Output folder and base name live in the Scene tab to avoid duplication."
    )
    info_label.setWordWrap(True)
    layout.addWidget(info_label)

    cge_group = QtGui.QGroupBox("Castle Engine")
    cge_layout = QtGui.QHBoxLayout(cge_group)
    cge_layout.addWidget(QtGui.QLabel("Ruta ejecutable / Executable path"))
    cge_layout.addStretch()
    layout.addWidget(cge_group)

    path_layout = QtGui.QHBoxLayout()
    cge_layout.addLayout(path_layout)
    path_layout.addWidget(QtGui.QLabel("Ruta / Path"))
    cge_path = QtGui.QLineEdit()
    path_layout.addWidget(cge_path)
    btn_browse = QtGui.QPushButton("Examinar / Browse")
    path_layout.addWidget(btn_browse)
    cge_path.setToolTip("ES: Selecciona el ejecutable de Castle Game Engine.\nEN: Select the Castle Game Engine executable.")

    options_group = QtGui.QGroupBox("Opciones globales / Global options")
    options_layout = QtGui.QVBoxLayout(options_group)
    chk_triangulate = QtGui.QCheckBox("Triangular mallas / Triangulate meshes")
    chk_freeze = QtGui.QCheckBox("Congelar colores en materiales / Freeze colors")
    chk_restore = QtGui.QCheckBox("Restaurar ultima sesion / Restore last session")
    options_layout.addWidget(chk_triangulate)
    options_layout.addWidget(chk_freeze)
    options_layout.addWidget(chk_restore)
    layout.addWidget(options_group)

    presets_group = QtGui.QGroupBox("Perfiles / Presets")
    presets_layout = QtGui.QVBoxLayout(presets_group)
    name_layout = QtGui.QHBoxLayout()
    name_layout.addWidget(QtGui.QLabel("Nombre / Name"))
    presets_name = QtGui.QLineEdit()
    name_layout.addWidget(presets_name)
    presets_layout.addLayout(name_layout)

    buttons_layout = QtGui.QHBoxLayout()
    btn_save = QtGui.QPushButton("Guardar / Save")
    btn_load = QtGui.QPushButton("Cargar / Load")
    buttons_layout.addWidget(btn_save)
    buttons_layout.addWidget(btn_load)
    presets_layout.addLayout(buttons_layout)

    sidecar_layout = QtGui.QHBoxLayout()
    sidecar_label = QtGui.QLabel("Sidecar: <DocStem>.gee.json")
    btn_force = QtGui.QPushButton("Forzar guardar / Force save")
    sidecar_layout.addWidget(sidecar_label)
    sidecar_layout.addWidget(btn_force)
    presets_layout.addLayout(sidecar_layout)
    layout.addWidget(presets_group)

    layout.addStretch()
    return tab


__all__ = ["build_config_tab"]
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
