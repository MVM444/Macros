import sys
import FreeCAD as App

repo = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad"
target = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
if repo not in sys.path:
    sys.path.insert(0, repo)

from FacilArquitecturaWB.core.room_utils import (
    collect_opening_sketches,
    create_closed_room_sketch,
    create_closed_wall_sketches,
)

doc = App.openDocument(target)
master = doc.getObject("FA_MasterSketches")
areas = doc.getObject("FA_Areas")
wall = doc.getObject("Sketch_Centros_Pared_Muro_Seco_Espesor_120mm")
doc.getObject("Sketch_Centros_Puertas").FA_CenterlineKind = "doors"
doc.getObject("Sketch_Centros_Ventanas").FA_CenterlineKind = "windows"
openings = collect_opening_sketches(doc)
print("OPENINGS", [(o.Name, len(o.Geometry)) for o in openings])
for name in ("Sketch_Centros_Puertas", "Sketch_Centros_Ventanas"):
    obj = doc.getObject(name)
    print("OPENING_DEBUG", name, [(p, str(getattr(obj, p, None))) for p in obj.PropertiesList if p.startswith("FA_")])

closed, close_summary = create_closed_wall_sketches(
    doc, master, [wall], openings,
    max_gap_mm=3000.0,
    alignment_tolerance_mm=25.0,
    angle_tolerance_deg=3.0,
    close_unmarked_gaps=True,
    replace_previous=True,
)
print("CLOSED", [(o.Name, len(o.Geometry), getattr(o, "FA_ClosedGapCount", None)) for o in closed])
print("CLOSE_SUMMARY", close_summary)

try:
    room, topology = create_closed_room_sketch(
        doc, areas, closed,
        snap_tolerance=75.0,
        minimum_room_area_m2=1.0,
        replace_previous=True,
    )
    print("ROOMS", room.Name, len(topology["faces"]), getattr(room, "FA_RoomAreas", []))
except Exception as exc:
    print("ROOM_WARNING", type(exc).__name__, str(exc))

doc.recompute()
doc.save()
print("SAVED", target, len(doc.Objects))
App.closeDocument(doc.Name)
