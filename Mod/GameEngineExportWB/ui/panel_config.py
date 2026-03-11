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
