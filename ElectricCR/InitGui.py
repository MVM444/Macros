# -*- coding: utf-8 -*-

import os
import FreeCAD as App
import FreeCADGui as Gui

BASE_DIR = os.path.dirname(__file__)
ICONS_DIR = os.path.join(BASE_DIR, "icons")


def icon_path(basename: str) -> str:
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
        # Evitar duplicados si se recarga el módulo
        if getattr(self, "_built", False):
            return

        # Asegurar que Draft registre sus comandos
        try:
            import Draft  # noqa: F401
            import DraftGui  # noqa: F401
        except Exception:
            pass

        available = set(Gui.listCommands())

        # Esbozar (dibujo)
        esbozar = [
            "Draft_Line", "Draft_Wire", "Draft_Fillet",
            "Draft_Arc", "Draft_Circle", "Draft_Ellipse", "Draft_Rectangle",
            "Draft_Polygon", "Draft_BSpline", "Draft_BezCurve",
            "Draft_Point", "Draft_Facebinder", "Draft_TextShape", "Draft_Hatch",
        ]

        # Anotación
        anotacion = ["Draft_Text", "Draft_Dimension", "Draft_Label", "Draft_AnnotationStyleEditor"]

        # Modificación (incluye matrices)
        modificacion = [
            "Draft_Move", "Draft_Rotate", "Draft_Scale", "Draft_Mirror",
            "Draft_Offset", "Draft_Trimex", "Draft_Stretch", "Draft_Edit",
            "Draft_Join", "Draft_Split", "Draft_Upgrade", "Draft_Downgrade",
            "Draft_Clone", "Draft_Array", "Draft_PathArray", "Draft_PolarArray",
            "Draft_Shape2DView",
        ]

        # Utilidades
        utilidades = [
            "Draft_SetStyle", "Draft_ApplyStyle", "Draft_Layer",
            "Draft_ToggleConstructionMode", "Draft_ToggleGrid", "Draft_SelectPlane",
            "Draft_AddToGroup", "Draft_MoveToGroup", "Draft_SelectGroup",
        ]

        groups = [
            ("Esbozar", [c for c in esbozar if c in available]),
            ("Anotación", [c for c in anotacion if c in available]),
            ("Modificación", [c for c in modificacion if c in available]),
            ("Utilidades", [c for c in utilidades if c in available]),
        ]

        for title, cmds in groups:
            if cmds:
                self.appendToolbar(title, cmds)
                self.appendMenu(title, cmds)

        # Registrar y añadir grupos de macros ElectricCR
        try:
            from .commands.macros import register_predefined_macros
            macro_groups = register_predefined_macros(BASE_DIR)
            for title, cmds in macro_groups:
                if cmds:
                    self.appendToolbar(title, cmds)
                    self.appendMenu(title, cmds)
        except Exception:
            pass

        self._built = True

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(ElectricCRWorkbench())

