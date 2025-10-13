"""Scene TaskPanel for Game Engine Export WB.

Descripcion rapida: panel principal con pestañas para escena, configuracion y texto informativo.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Mantener interfaz bilingue ES/EN con cadenas ASCII.
- Respetar requisitos de escala, rotacion, GameStart y luces en futuras implementaciones.
- Mostrar mensajes en consola con prefijo [GAMEEXPORT] para depuracion.
- Evitar logica de exportacion aun, solo estructura y placeholders.
"""

from PySide import QtCore, QtGui

from . import panel_config
from . import panel_info


class TaskPanel:
    """Main TaskPanel with tabs for scene setup, config and information."""

    def __init__(self):
        FreeCAD = __import__("FreeCAD")
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Building TaskPanel widgets\n")
        self.widget = QtGui.QWidget()
        self.widget.setWindowTitle("Game Engine Export")
        layout = QtGui.QVBoxLayout(self.widget)
        self.tab = QtGui.QTabWidget()
        layout.addWidget(self.tab)

        self.scene_tab = self._build_scene_tab()
        self.config_tab = panel_config.build_config_tab()
        self.info_tab = panel_info.build_info_tab()

        self.tab.addTab(self.scene_tab, "Escena / Scene")
        self.tab.addTab(self.config_tab, "Config & Profiles")
        self.tab.addTab(self.info_tab, "Informacion / Information")

    def _build_scene_tab(self):
        """Create widgets for the scene tab."""
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)

        root_group = QtGui.QGroupBox("Raiz / Root")
        root_layout = QtGui.QHBoxLayout(root_group)
        self.root_line = QtGui.QLineEdit()
        self.root_line.setReadOnly(True)
        root_layout.addWidget(self.root_line)
        self.btn_use_selection = QtGui.QPushButton("Tomar seleccion / Use selection")
        self.btn_use_selection.setToolTip("ES: Establece el grupo principal de la escena.\nEN: Set the main scene group.")
        root_layout.addWidget(self.btn_use_selection)
        layout.addWidget(root_group)

        objects_group = QtGui.QGroupBox("Objetos / Objects")
        objects_layout = QtGui.QVBoxLayout(objects_group)
        list_layout = QtGui.QHBoxLayout()
        self.list_available = QtGui.QListWidget()
        self.list_available.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        list_layout.addWidget(self.list_available)
        btn_layout = QtGui.QVBoxLayout()
        self.btn_move_right = QtGui.QPushButton(">>")
        self.btn_move_left = QtGui.QPushButton("<<")
        btn_layout.addWidget(self.btn_move_right)
        btn_layout.addWidget(self.btn_move_left)
        btn_layout.addStretch()
        list_layout.addLayout(btn_layout)
        self.list_export = QtGui.QListWidget()
        self.list_export.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        list_layout.addWidget(self.list_export)
        objects_layout.addLayout(list_layout)

        actions_layout = QtGui.QHBoxLayout()
        self.btn_refresh = QtGui.QPushButton("Actualizar lista / Refresh list")
        self.btn_refresh.setToolTip("ES: Escanea subarbol y actualiza los objetos disponibles.\nEN: Scan subtree and refresh available objects.")
        self.btn_clear = QtGui.QPushButton("Limpiar lista / Clear list")
        actions_layout.addWidget(self.btn_refresh)
        actions_layout.addWidget(self.btn_clear)
        objects_layout.addLayout(actions_layout)

        info_label = QtGui.QLabel("ES: Si la lista A exportar queda vacia se exporta todo el subarbol.\nEN: If the To export list is empty the whole subtree is exported.")
        info_label.setWordWrap(True)
        objects_layout.addWidget(info_label)
        layout.addWidget(objects_group)

        gamestart_group = QtGui.QGroupBox("GameStart")
        gamestart_layout = QtGui.QHBoxLayout(gamestart_group)
        self.gamestart_line = QtGui.QLineEdit()
        self.gamestart_line.setText("GameStart")
        gamestart_layout.addWidget(self.gamestart_line)
        self.btn_create_gamestart = QtGui.QPushButton("Crear / Create")
        gamestart_layout.addWidget(self.btn_create_gamestart)
        self.label_gamestart_state = QtGui.QLabel("GameStart no encontrado")
        gamestart_layout.addWidget(self.label_gamestart_state)
        self.btn_create_gamestart.setToolTip("ES: Crea un marcador (cono+base). Sus propiedades definen el Viewpoint inicial.\nEN: Creates a marker (cone+base). Its properties define the initial Viewpoint.")
        layout.addWidget(gamestart_group)

        light_group = QtGui.QGroupBox("Luz global / Global light")
        light_layout = QtGui.QGridLayout(light_group)
        self.chk_global_light = QtGui.QCheckBox("Habilitar / Enable")
        light_layout.addWidget(self.chk_global_light, 0, 0, 1, 2)
        light_layout.addWidget(QtGui.QLabel("Yaw (deg)"), 1, 0)
        self.spin_gl_yaw = QtGui.QDoubleSpinBox()
        self.spin_gl_yaw.setRange(-360.0, 360.0)
        light_layout.addWidget(self.spin_gl_yaw, 1, 1)
        light_layout.addWidget(QtGui.QLabel("Pitch (deg)"), 2, 0)
        self.spin_gl_pitch = QtGui.QDoubleSpinBox()
        self.spin_gl_pitch.setRange(-360.0, 360.0)
        light_layout.addWidget(self.spin_gl_pitch, 2, 1)
        light_layout.addWidget(QtGui.QLabel("Intensidad / Intensity"), 3, 0)
        self.spin_gl_intensity = QtGui.QDoubleSpinBox()
        self.spin_gl_intensity.setRange(0.0, 5.0)
        self.spin_gl_intensity.setSingleStep(0.1)
        light_layout.addWidget(self.spin_gl_intensity, 3, 1)
        self.btn_gl_color = QtGui.QPushButton("Color... / Color...")
        light_layout.addWidget(self.btn_gl_color, 4, 0)
        self.btn_gl_time = QtGui.QPushButton("Hora solar... / Solar time...")
        light_layout.addWidget(self.btn_gl_time, 4, 1)
        self.chk_global_light.setToolTip("ES: DirectionalLight con direccion a partir de yaw/pitch.\nEN: DirectionalLight; direction from yaw/pitch.")
        layout.addWidget(light_group)

        lights_group = QtGui.QGroupBox("Luces de escena / Scene lights")
        lights_layout = QtGui.QVBoxLayout(lights_group)
        self.chk_pointlights = QtGui.QCheckBox("Exportar PointLights / Export point lights")
        lights_layout.addWidget(self.chk_pointlights)
        btn_lights_layout = QtGui.QHBoxLayout()
        self.btn_add_light = QtGui.QPushButton("Agregar seleccion como luz / Add selection as light")
        self.btn_remove_light = QtGui.QPushButton("Quitar seleccion como luz / Remove selection as light")
        btn_lights_layout.addWidget(self.btn_add_light)
        btn_lights_layout.addWidget(self.btn_remove_light)
        lights_layout.addLayout(btn_lights_layout)
        layout.addWidget(lights_group)

        output_group = QtGui.QGroupBox("Salida / Output")
        output_layout = QtGui.QGridLayout(output_group)
        output_layout.addWidget(QtGui.QLabel("Carpeta / Folder"), 0, 0)
        self.output_dir_line = QtGui.QLineEdit()
        output_layout.addWidget(self.output_dir_line, 0, 1)
        self.btn_output_browse = QtGui.QPushButton("Examinar / Browse")
        output_layout.addWidget(self.btn_output_browse, 0, 2)
        output_layout.addWidget(QtGui.QLabel("Nombre base / Base name"), 1, 0)
        self.output_base_line = QtGui.QLineEdit()
        output_layout.addWidget(self.output_base_line, 1, 1, 1, 2)
        self.chk_launch_cge = QtGui.QCheckBox("Lanzar Castle Engine al exportar / Launch CGE after export")
        output_layout.addWidget(self.chk_launch_cge, 2, 0, 1, 3)
        layout.addWidget(output_group)

        self.btn_export = QtGui.QPushButton("Exportar X3D / Export X3D")
        self.btn_export.setToolTip("ES: Exporta a X3D con mm->m y rotacion -90 X; inserta Viewpoint y luces.\nEN: Export to X3D with mm->m and -90 X rotation; inserts Viewpoint and lights.")
        layout.addWidget(self.btn_export)

        footer = QtGui.QLabel(
            "ES: FreeCAD trabaja en mm; el X3D usa metros y aplica rotacion -90 en X. Evita acentos en nombres.\n"
            "EN: FreeCAD works in mm; output X3D uses meters with -90 X rotation. Avoid accents in names."
        )
        footer.setWordWrap(True)
        layout.addWidget(footer)

        layout.addStretch()
        return tab

    def getStandardButtons(self):
        """FreeCAD TaskPanel API: hide standard buttons."""
        return int(QtGui.QDialogButtonBox.Close)

    def accept(self):
        """Handle dialog accept (placeholder)."""
        FreeCAD = __import__("FreeCAD")
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Accept pressed (no action)\n")

    def reject(self):
        """Handle dialog reject."""
        FreeCAD = __import__("FreeCAD")
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Reject pressed\n")


__all__ = ["TaskPanel"]
