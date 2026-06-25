# -*- coding: utf-8 -*-
"""GUI bootstrap for development-layout resource paths."""

import os
import sys

try:
    import FreeCAD as App
except Exception:
    App = None

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


def _macro_path_entries():
    entries = []
    if App is not None:
        try:
            param = App.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath", "")
        except Exception:
            param = ""
        if param:
            sep = ";" if os.name == "nt" else ":"
            for part in param.split(sep):
                part = part.strip()
                if part:
                    full = os.path.normpath(os.path.abspath(part))
                    if full not in entries:
                        entries.append(full)
        try:
            macro_dir = App.getUserMacroDir()
        except Exception:
            macro_dir = ""
        if macro_dir:
            full = os.path.normpath(os.path.abspath(macro_dir))
            if full not in entries:
                entries.append(full)
    return entries


def _here_dir():
    path = globals().get("__file__", "")
    if not path:
        module = sys.modules.get(__name__)
        path = getattr(module, "__file__", "") if module is not None else ""
    if path:
        return os.path.abspath(os.path.dirname(path))
    for base in _macro_path_entries():
        candidate = os.path.join(base, "Mod", "DevPathsBootstrap")
        if os.path.isdir(candidate):
            return os.path.abspath(candidate)
    return os.getcwd()


_HERE = _here_dir()
_MOD_ROOT = os.path.abspath(os.path.dirname(_HERE))
_MACRO_ROOT = os.path.abspath(os.path.dirname(_MOD_ROOT))
_DEV_ROOT = os.path.join(_MACRO_ROOT, "Macros-de-Freecad")

_add_icon_path(os.path.join(_DEV_ROOT, "ElectricCR", "icons"))
