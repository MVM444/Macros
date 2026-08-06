import sys
import statistics
import FreeCAD as App

repo = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad"
if repo not in sys.path:
    sys.path.insert(0, repo)

path = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
doc = App.openDocument(path)

def bounds(obj):
    shape = getattr(obj, "Shape", None)
    if shape is None or shape.isNull():
        return None
    b = shape.BoundBox
    return (b.XMin, b.YMin, b.XMax, b.YMax, b.XLength, b.YLength, b.ZLength)

for name in (
    "Sketch_Centros_Pared_Muro_Seco_Espesor_120mm",
    "Sketch_Centros_Puertas",
    "Sketch_Centros_Ventanas",
    "Sketch_Centros_P4",
    "Sketch_Centros_P4_Columnas",
    "Wall",
    "Structure001",
    "FA_TestTerrain",
):
    obj = doc.getObject(name)
    print("BOUNDS", name, bounds(obj) if obj else None)

for name in ("Sketch_Centros_Puertas", "Sketch_Centros_Ventanas", "Sketch_Centros_Pared_Muro_Seco_Espesor_120mm"):
    obj = doc.getObject(name)
    lengths = []
    for geo in list(obj.Geometry):
        if hasattr(geo, "StartPoint") and hasattr(geo, "EndPoint"):
            lengths.append((geo.EndPoint - geo.StartPoint).Length)
    print("LENGTHS", name, "count", len(lengths), "min", min(lengths), "median", statistics.median(lengths), "max", max(lengths), "values", sorted(round(v, 2) for v in lengths))

wall = doc.getObject("Wall")
print("WALL_WIDTH", getattr(wall, "Width", None), "WALL_HEIGHT", getattr(wall, "Height", None))
App.closeDocument(doc.Name)
