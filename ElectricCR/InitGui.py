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

        # Añadir barras y menús (solo si hay comandos disponibles)
        if draft_available:
            self.appendToolbar("Herramientas Draft", draft_available)
            self.appendMenu("Herramientas Draft", draft_available)

        self.appendToolbar("Herramientas Electric", custom_commands)
        self.appendMenu("Electric", custom_commands)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(ElectricCRWorkbench())
