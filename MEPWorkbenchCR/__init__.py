# -*- coding: utf-8 -*-
"""Root shim for the development-layout MEPWorkbenchCR package."""

import importlib.util
import os
import sys


_HERE = os.path.abspath(os.path.dirname(__file__))
_REPO_ROOT = os.path.abspath(os.path.dirname(_HERE))
_REAL_PARENT = os.path.join(_REPO_ROOT, "Macros-de-Freecad")
_REAL_PACKAGE = os.path.join(_REAL_PARENT, "MEPWorkbenchCR")
_REAL_INIT = os.path.join(_REAL_PACKAGE, "Init.py")

if _REAL_PARENT not in sys.path and os.path.isdir(_REAL_PARENT):
    sys.path.insert(0, _REAL_PARENT)

__path__ = [_HERE]
if os.path.isdir(_REAL_PACKAGE) and _REAL_PACKAGE not in __path__:
    __path__.append(_REAL_PACKAGE)


def _run_real_bootstrap():
    if not os.path.isfile(_REAL_INIT):
        return
    try:
        spec = importlib.util.spec_from_file_location("_mepworkbenchcr_real_bootstrap", _REAL_INIT)
        if spec is None or spec.loader is None:
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        return


_run_real_bootstrap()
