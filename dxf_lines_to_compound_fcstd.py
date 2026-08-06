"""Create a lightweight FCStd containing DXF LINE entities in one compound."""

import sys

import FreeCAD
import Part


def records(path):
    with open(path, encoding="ascii", errors="replace") as stream:
        lines = [line.rstrip("\r\n") for line in stream]
    return [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines) - 1, 2)]


source, target = sys.argv[1], sys.argv[2]
pairs = records(source)
edges = []
i = 0
while i < len(pairs):
    if pairs[i] == ("0", "LINE"):
        values = {}
        i += 1
        while i < len(pairs) and pairs[i][0] != "0":
            values[pairs[i][0]] = pairs[i][1]
            i += 1
        a = FreeCAD.Vector(float(values["10"]), float(values["20"]), 0)
        b = FreeCAD.Vector(float(values["11"]), float(values["21"]), 0)
        # Sub-50 mm segments are predominantly hatch/detail noise and make the
        # compound unnecessarily heavy without affecting the building outline.
        if (b - a).Length >= 50.0:
            edges.append(Part.makeLine(a, b))
        continue
    i += 1

doc = FreeCAD.newDocument("Mejoras_1411_04")
obj = doc.addObject("Part::Feature", "Planta_vectorial")
obj.Label = "Planta vectorial - escala real en mm"
obj.Shape = Part.makeCompound(edges)
obj.addProperty("App::PropertyString", "Fuente", "Conversion")
obj.Fuente = source
obj.addProperty("App::PropertyString", "EscalaAplicada", "Conversion")
obj.EscalaAplicada = "1:50 (factor 50 sobre el papel)"
doc.recompute()
doc.saveAs(target)
print("Saved", target, "compound edges", len(edges))
