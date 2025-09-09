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

        # Lista de comandos Draft comunes
        draft_commands = [
            "Draft_SelectPlane",
            "Draft_Point",
            "Draft_Line",
            "Draft_Wire",
            "Draft_Circle",
            "Draft_Arc",
            "Draft_Ellipse",
            "Draft_Rectangle",
            "Draft_Polygon",
            "Draft_Text",
            "Draft_Dimension",
            "Draft_Move",
            "Draft_Rotate",
            "Draft_Scale",
            "Draft_Mirror",
            "Draft_Offset",
            "Draft_Trimex",
            "Draft_Join",
            "Draft_Split",
            "Draft_Upgrade",
            "Draft_Downgrade",
            "Draft_Array",
            "Draft_PathArray",
            "Draft_PolarArray",
            "Draft_Clone",
            "Draft_Shape2DView",
            "Draft_Facebinder",
            "Draft_Edit",
        ]

        # Filtrar solo los comandos disponibles para evitar "Unknown command"
        available = set(Gui.listCommands())
        draft_available = [c for c in draft_commands if c in available]

        # Importar y registrar comandos personalizados
        from .commands.insert_outlet import COMMAND_NAME as INSERT_OUTLET_CMD

        custom_commands = [INSERT_OUTLET_CMD]

        # Añadir barras y menús (solo si hay comandos disponibles)
        if draft_available:
            self.appendToolbar("Herramientas Draft", draft_available)
            self.appendMenu("Herramientas Draft", draft_available)

        self.appendToolbar("Herramientas Electric", custom_commands)
        self.appendMenu("Electric", custom_commands)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(ElectricCRWorkbench())
