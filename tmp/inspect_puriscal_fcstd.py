import FreeCAD as App
from collections import Counter

path = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Versión 2.FCStd"
doc = App.openDocument(path)
objects = list(doc.Objects)
print("OBJECTS", len(objects))
print("TYPES", Counter(obj.TypeId for obj in objects).most_common(30))
groups = []
for obj in objects:
    if hasattr(obj, "Group"):
        groups.append((obj.Name, obj.Label, len(list(obj.Group or []))))
print("GROUPS", groups)
shapes = [obj for obj in objects if hasattr(obj, "Shape") and not obj.Shape.isNull()]
print("SHAPES", len(shapes))
for obj in objects:
    label = str(getattr(obj, "Label", ""))
    name = str(getattr(obj, "Name", ""))
    if any(key in (label + " " + name).lower() for key in ("muro", "wall", "puerta", "door", "ventana", "window", "column", "eje")):
        print("MATCH", obj.TypeId, name, repr(label), len(list(getattr(obj, "Group", []) or [])))
App.closeDocument(doc.Name)
