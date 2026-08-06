import os
import sys

import FreeCAD as App

repo = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad"
source = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Versión 2.FCStd"
target = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
if repo not in sys.path:
    sys.path.insert(0, repo)

from FacilArquitecturaWB.core.room_utils import collect_room_source_sketches, create_closed_room_sketch
from FacilArquitecturaWB.core.site_floor_utils import collect_plan_sketches, create_site_floor_from_sketches

doc = App.openDocument(source)
doc.saveAs(target)

bim_group = doc.getObject("FA_BIM")
areas_group = doc.getObject("FA_Areas")
if bim_group is None or areas_group is None:
    raise RuntimeError("El proyecto Facil Arquitectura no contiene los grupos BIM/Areas esperados.")

plan_sketches = collect_plan_sketches(doc)
print("PLAN_SOURCES", [(obj.Name, obj.Label, len(obj.Geometry)) for obj in plan_sketches])

room_result = None
try:
    room_sources = collect_room_source_sketches(doc)
    room_sketch, topology = create_closed_room_sketch(
        doc,
        areas_group,
        room_sources,
        snap_tolerance=50.0,
        minimum_room_area_m2=1.0,
        replace_previous=True,
    )
    room_result = (room_sketch.Name, len(topology["faces"]), len(topology["edges"]))
except Exception as exc:
    print("ROOM_WARNING", type(exc).__name__, str(exc))

site_result = create_site_floor_from_sketches(
    doc,
    bim_group,
    plan_sketches,
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
doc.save()
print("ROOM_RESULT", room_result)
print("SITE_RESULT", {key: (value.Name if value is not None else None) for key, value in site_result.items()})
print("FINAL_OBJECTS", len(doc.Objects))
print("TARGET", target)
App.closeDocument(doc.Name)
