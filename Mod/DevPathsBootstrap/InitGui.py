# -*- coding: utf-8 -*-
"""GUI bootstrap for development-layout resource paths."""

import os

try:
    import FreeCADGui as Gui
except Exception:
    Gui = None


def _add_icon_path(path):
    if Gui is None or not path or not os.path.isdir(path):
        return
    try:
        Gui.addIconPath(path.replace(os.sep, "/"))
    except Exception:
        pass


_HERE = os.path.abspath(os.path.dirname(__file__))
_MOD_ROOT = os.path.abspath(os.path.dirname(_HERE))
_MACRO_ROOT = os.path.abspath(os.path.dirname(_MOD_ROOT))
_DEV_ROOT = os.path.join(_MACRO_ROOT, "Macros-de-Freecad")

_add_icon_path(os.path.join(_DEV_ROOT, "ElectricCR", "icons"))
