# -*- coding: utf-8 -*-

import os
import FreeCAD as App
import FreeCADGui as Gui

BASE_DIR = os.path.dirname(__file__)
ICONS_DIR = os.path.join(BASE_DIR, "icons")

# Intentar resolver un icono por nombre base (.svg, .png) o nombre completo.
def icon_path(basename):
    candidates = [f"{basename}.svg", f"{basename}.png", basename]
    for candidate in candidates:
        path = os.path.join(ICONS_DIR, candidate)
        if os.path.exists(path):
            return path
    return ""


class ElectricCRWorkbench(Gui.Workbench):
    """Workbench personalizado ElectricCR"""

    MenuText = "Eléctrico CR"
    ToolTip = "Workbench para diseñar instalaciones eléctricas"
    Icon = icon_path("Rayo")

    def Initialize(self):
        # Intentar cargar Draft (si existe) para registrar comandos
        try:
            import Draft  # noqa: F401
            import DraftGui  # noqa: F401
        except Exception:
            pass

        # Detectar dinámicamente todos los comandos Draft disponibles
        available = list(Gui.listCommands())
        draft_available = sorted([c for c in available if c.startswith("Draft_")])

        # Importar y registrar comandos personalizados
        from .commands.insert_outlet import COMMAND_NAME as INSERT_OUTLET_CMD

        custom_commands = [INSERT_OUTLET_CMD]

        # Agrupar comandos Draft y crear barras/menus ordenados
        try:
            _available = set(Gui.listCommands())
            draft_draw = [
                "Draft_SelectPlane", "Draft_Point", "Draft_Line", "Draft_Wire",
                "Draft_Circle", "Draft_Arc", "Draft_Ellipse", "Draft_Rectangle",
                "Draft_Polygon", "Draft_Text",
            ]
            draft_modify = [
                "Draft_Move", "Draft_Rotate", "Draft_Scale", "Draft_Mirror",
                "Draft_Offset", "Draft_Trimex", "Draft_Join", "Draft_Split",
                "Draft_Upgrade", "Draft_Downgrade", "Draft_Edit",
            ]
            draft_arrays = ["Draft_Array", "Draft_PathArray", "Draft_PolarArray", "Draft_Clone"]
            draft_annotation = ["Draft_Dimension", "Draft_Shape2DView", "Draft_Facebinder"]

            draft_groups = [
                ("Draft • Dibujo", [c for c in draft_draw if c in _available]),
                ("Draft • Modificar", [c for c in draft_modify if c in _available]),
                ("Draft • Matrices", [c for c in draft_arrays if c in _available]),
                ("Draft • Anotacion", [c for c in draft_annotation if c in _available]),
            ]

            for title, cmds in draft_groups:
                if cmds:
                    self.appendToolbar(title, cmds)
                    self.appendMenu(title, cmds)
        except Exception:
            pass

        # Registrar macros de ElectricCR como comandos y agruparlas
        try:
            from .commands.macros import register_predefined_macros
            macro_groups = register_predefined_macros(BASE_DIR)
            for title, cmds in macro_groups:
                if cmds:
                    self.appendToolbar(title, cmds)
                    self.appendMenu(title, cmds)
        except Exception:
            pass

        # Añadir barras y menús (solo si hay comandos disponibles)
        # Deshabilitar barra Draft plana (usamos las agrupadas arriba)
        draft_available = []
        if draft_available:
            self.appendToolbar("Herramientas Draft", draft_available)
            self.appendMenu("Herramientas Draft", draft_available)

        self.appendToolbar("Electric • Basico", custom_commands)
        self.appendMenu("Electric • Basico", custom_commands)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(ElectricCRWorkbench())
