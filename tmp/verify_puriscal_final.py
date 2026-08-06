import FreeCAD as App

path = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
doc = App.openDocument(path)
names = [
    "FA_Project",
    "Spreadsheet_Parametros",
    "Sketch_Centros_Pared_Muro_Seco_Espesor_120mm",
    "Sketch_Centros_Puertas",
    "Sketch_Centros_Ventanas",
    "Sketch_Centros_P4_Columnas",
    "Wall",
    "AxisSystem",
    "Structure",
    "FA_FloorFootprint",
    "Structure001",
    "FA_TestTerrain",
    "Site",
    "Sketch_Cerrado_Sketch_Centros_Pared_Muro_Seco_Espesor_120mm",
]
for name in names:
    obj = doc.getObject(name)
    shape = getattr(obj, "Shape", None) if obj else None
    print("CHECK", name, bool(obj), getattr(obj, "TypeId", None), bool(shape and not shape.isNull()))
print("KINDS", doc.getObject("Sketch_Centros_Puertas").FA_CenterlineKind, doc.getObject("Sketch_Centros_Ventanas").FA_CenterlineKind)
closed = doc.getObject("Sketch_Cerrado_Sketch_Centros_Pared_Muro_Seco_Espesor_120mm")
print("CLOSED_GAPS", closed.FA_ClosedGapCount)
print("TOTAL", len(doc.Objects), "FILE", doc.FileName)
App.closeDocument(doc.Name)
