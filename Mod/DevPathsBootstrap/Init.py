# -*- coding: utf-8 -*-
"""Early bootstrap for development-layout workbenches in this Macros repo.

FreeCAD can restore document proxies before macro loaders are executed. This
module is placed under ``Mod`` so FreeCAD sees it during startup and can add
the repository development paths to ``sys.path`` early.
"""

import importlib
import os
import sys


def _candidate_paths():
    here = os.path.abspath(os.path.dirname(__file__))
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
