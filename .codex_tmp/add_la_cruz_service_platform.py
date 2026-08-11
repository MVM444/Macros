import os
import sys

import FreeCAD as App


PACKAGE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Macros-de-Freecad",
    "FacilArquitecturaWB",
)
REPO_DIR = os.path.dirname(PACKAGE_DIR)
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)

from FacilArquitecturaWB.modules.service_platform.builder import (  # noqa: E402
    create_service_platform_front,
)
from FacilArquitecturaWB.modules.service_platform.model import PlatformOptions  # noqa: E402


SOURCE = os.environ["FA_PLATFORM_SOURCE"]
OUTPUT = os.environ["FA_PLATFORM_OUTPUT"]


def find_level(doc):
    for obj in doc.Objects:
        if str(getattr(obj, "FA_Role", "") or "") == "level":
            return obj
        if str(getattr(obj, "IfcType", "") or "") == "Building Storey":
            return obj
    return None


doc = App.openDocument(SOURCE)
doc.openTransaction("FA Agregar plataforma La Cruz")
options = PlatformOptions(
    total_width_mm=3000.0,
    service_positions=2,
    desk_depth_mm=600.0,
    desk_height_mm=740.0,
    desk_thickness_mm=30.0,
    side_margin_mm=0.0,
    divider_thickness_mm=40.0,
    divider_depth_mm=600.0,
    divider_height_mm=450.0,
    staff_zone_depth_mm=1800.0,
    public_zone_depth_mm=1500.0,
    origin_x_mm=8457.343,
    front_offset_mm=8953.318,
    minimum_position_width_mm=1200.0,
    create_3d_furniture=True,
    create_functional_zones=True,
)
result = create_service_platform_front(doc, options)
root = result["root"]
root.Label = "Plataforma de atencion - 2 puestos / 3000 mm"
axis = result["sketches"]["SK_PA_FrontAxis"]
axis.Label = "Sketch centro plataforma - 2 puestos / 3000 mm"
level = find_level(doc)
if level is not None:
    level.addObject(root)
doc.recompute()
doc.commitTransaction()

assert root.FA_IncludeCashier is False
assert int(root.FA_ServicePositions) == 2
assert abs(float(root.FA_TotalWidth_mm) - 3000.0) < 0.01
assert len(axis.Geometry) == 1
line = axis.Geometry[0]
assert abs(float(line.StartPoint.x) - 8457.343) < 0.01
assert abs(float(line.EndPoint.x) - 11457.343) < 0.01
assert abs(float(line.StartPoint.y) - 8953.318) < 0.01
assert abs(float(line.EndPoint.y) - 8953.318) < 0.01
assert len(result["geometry"]["desks"]) == 2
assert len(result["geometry"]["dividers"]) == 1
doc.saveAs(OUTPUT)
root_name = root.Name
axis_name = axis.Name
level_name = level.Name if level is not None else ""
App.closeDocument(doc.Name)

reopened = App.openDocument(OUTPUT)
reopened.recompute()
restored_root = reopened.getObject(root_name)
restored_axis = reopened.getObject(axis_name)
assert restored_root is not None
assert restored_axis is not None and len(restored_axis.Geometry) == 1
assert restored_root.FA_IncludeCashier is False
assert int(restored_root.FA_ServicePositions) == 2
if level_name:
    restored_level = reopened.getObject(level_name)
    assert restored_level is not None and restored_root in list(restored_level.Group)
generated = [
    obj
    for obj in reopened.Objects
    if str(getattr(obj, "FA_GeneratedBy", "") or "") == "FA_CreateServicePlatformFront"
]
assert len(generated) == 14, len(generated)
App.closeDocument(reopened.Name)
print(
    "LA_CRUZ_PLATFORM_OK",
    "axis=(8457.343,8953.318)-(11457.343,8953.318)",
    "positions=2 width=3000 cashier=false generated=14 persistence=ok",
    OUTPUT,
    flush=True,
)
