# -*- coding: utf-8 -*-
"""Early bootstrap for development-layout workbenches in this Macros repo.

FreeCAD can restore document proxies before macro loaders are executed. This
module is placed under ``Mod`` so FreeCAD sees it during startup and can add
the repository development paths to ``sys.path`` early.
"""

import importlib
import os
import sys

import FreeCAD as App


def _candidate_paths():
    source = globals().get("__file__", "")
    if not source:
        module = sys.modules.get(__name__)
        source = getattr(module, "__file__", "") if module is not None else ""
    if source:
        here = os.path.abspath(os.path.dirname(source))
    else:
        here = ""
        try:
            macro_path = App.ParamGet(
                "User parameter:BaseApp/Preferences/Macro"
            ).GetString("MacroPath", "")
        except Exception:
            macro_path = ""
        separator = ";" if os.name == "nt" else os.pathsep
        for base in [part.strip() for part in macro_path.split(separator) if part.strip()]:
            candidate = os.path.join(os.path.abspath(base), "Mod", "DevPathsBootstrap")
            if os.path.isdir(candidate):
                here = candidate
                break
        if not here:
            return []
    mod_root = os.path.abspath(os.path.dirname(here))
    macro_root = os.path.abspath(os.path.dirname(mod_root))
    repo_root = macro_root
    dev_root = os.path.join(repo_root, "Macros-de-Freecad")
    out = []
    for path in (macro_root, dev_root):
        if path and os.path.isdir(path) and path not in out:
            out.append(path)
    return out


for _path in _candidate_paths():
    if _path not in sys.path:
        sys.path.insert(0, _path)

importlib.invalidate_caches()

for _module_name in ("ElectricCR", "MEPWorkbenchCR", "MEPWorkbenchCR.Init", "MEP"):
    try:
        importlib.import_module(_module_name)
    except Exception:
        continue
