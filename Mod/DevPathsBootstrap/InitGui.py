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


_path = globals().get("__file__", "")
if not _path:
    _module = sys.modules.get(__name__)
    _path = getattr(_module, "__file__", "") if _module is not None else ""

_macro_paths = []
if App is not None:
    try:
        _param = App.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath", "")
    except Exception:
        _param = ""
    if _param:
        _sep = ";" if os.name == "nt" else ":"
        for _part in _param.split(_sep):
            _part = _part.strip()
            if _part:
                _full = os.path.normpath(os.path.abspath(_part))
                if _full not in _macro_paths:
                    _macro_paths.append(_full)
    try:
        _macro_dir = App.getUserMacroDir()
    except Exception:
        _macro_dir = ""
    if _macro_dir:
        _full = os.path.normpath(os.path.abspath(_macro_dir))
        if _full not in _macro_paths:
            _macro_paths.append(_full)

if _path:
    _HERE = os.path.abspath(os.path.dirname(_path))
else:
    _HERE = ""
    for _base in _macro_paths:
        _candidate = os.path.join(_base, "Mod", "DevPathsBootstrap")
        if os.path.isdir(_candidate):
            _HERE = os.path.abspath(_candidate)
            break
    if not _HERE:
        _HERE = os.getcwd()

_MOD_ROOT = os.path.abspath(os.path.dirname(_HERE))
_MACRO_ROOT = os.path.abspath(os.path.dirname(_MOD_ROOT))
_DEV_ROOT = os.path.join(_MACRO_ROOT, "Macros-de-Freecad")
_ICON_PATH = os.path.join(_DEV_ROOT, "ElectricCR", "icons")

if Gui is not None and os.path.isdir(_ICON_PATH):
    try:
        Gui.addIconPath(_ICON_PATH.replace(os.sep, "/"))
    except Exception:
        pass

# Load the neutral global Programacion toolbar independently of all workbenches.
_PROGRAMACION_DIR = os.path.join(_MACRO_ROOT, "Programación")
_PROGRAMACION_LOADER = os.path.join(_PROGRAMACION_DIR, "programacion_toolbar.py")
if Gui is not None and os.path.isfile(_PROGRAMACION_LOADER):
    try:
        if _PROGRAMACION_DIR not in sys.path:
            sys.path.insert(0, _PROGRAMACION_DIR)
        import programacion_toolbar
        programacion_toolbar.install(_PROGRAMACION_DIR)
    except Exception as _programacion_error:
        if App is not None:
            App.Console.PrintError(
                "[PROGRAMACION][AUTOLOAD][ERROR] {}\n".format(_programacion_error)
            )
