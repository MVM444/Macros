# -*- coding: utf-8 -*-
"""Shim package to ensure ElectricCR modules are discoverable.

This folder is used for logs; we extend the package path to include the
real workbench package under Macros-de-Freecad if needed.
"""

import os
import sys
import pkgutil

_here = os.path.dirname(__file__)
_candidate = os.path.join(os.path.dirname(_here), "Macros-de-Freecad", "ElectricCR")
_parent = os.path.dirname(_candidate)

try:
    if os.path.isdir(_candidate) and _parent not in sys.path:
        sys.path.insert(0, _parent)
except Exception:
    pass

__path__ = pkgutil.extend_path(__path__, __name__)
