import sys
import FreeCAD as App

repo = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad"
model = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
if repo not in sys.path:
    sys.path.insert(0, repo)

from FacilArquitecturaWB.core.site_floor_utils import create_site_floor_from_sketches

doc = App.openDocument(model)
bim_group = doc.getObject("FA_BIM")
sources = [
    doc.getObject("Sketch_Centros_Pared_Muro_Seco_Espesor_120mm"),
    doc.getObject("Sketch_Centros_Puertas"),
    doc.getObject("Sketch_Centros_Ventanas"),
]
if bim_group is None or any(obj is None for obj in sources):
    raise RuntimeError("Faltan el grupo BIM o los sketches arquitectónicos esperados.")

result = create_site_floor_from_sketches(
    doc,
    bim_group,
    sources,
    {
        "floor_overhang_mm": 100.0,
        "floor_top_z_mm": 0.0,
        "floor_thickness_mm": 150.0,
        "create_test_terrain": True,
        "terrain_margin_mm": 5000.0,
        "pad_margin_mm": 1000.0,
        "terrain_variation_mm": 350.0,
        "terrain_seed": 1211,
        "replace_previous": True,
    },
)

doc.recompute()
for key in ("footprint", "slab", "terrain"):
    obj = result.get(key)
    if obj is None or not hasattr(obj, "Shape") or obj.Shape.isNull():
        print("BOUNDS", key, None)
        continue
    box = obj.Shape.BoundBox
    print("BOUNDS", key, box.XLength, box.YLength, box.ZLength)
print("SOURCES", [obj.Name for obj in sources])
doc.save()
print("SAVED", doc.FileName)
App.closeDocument(doc.Name)
