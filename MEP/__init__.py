# -*- coding: utf-8 -*-
"""Legacy shim for documents that still import ``MEP.*`` directly."""

import importlib
import os
import sys


_HERE = os.path.abspath(os.path.dirname(__file__))
_REPO_ROOT = os.path.abspath(os.path.dirname(_HERE))
_REAL_PARENT = os.path.join(_REPO_ROOT, "Macros-de-Freecad")

if _REAL_PARENT not in sys.path and os.path.isdir(_REAL_PARENT):
    sys.path.insert(0, _REAL_PARENT)

_real_pkg = importlib.import_module("MEPWorkbenchCR.MEP")
__path__ = list(getattr(_real_pkg, "__path__", []))
