"""FreeCAD command-line helper: import a DXF and save it as FCStd."""

import sys

import FreeCAD
import importDXF


source, target = sys.argv[1], sys.argv[2]
doc = FreeCAD.newDocument("Mejoras_1411_04")
importDXF.insert(source, doc.Name)
doc.recompute()
doc.saveAs(target)
print("Saved", target, "objects", len(doc.Objects))
