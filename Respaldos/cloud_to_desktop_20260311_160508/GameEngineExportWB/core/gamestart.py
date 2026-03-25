<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
"""GameStart utilities for Game Engine Export WB.

Descripcion rapida: creacion, busqueda y lectura de metadatos de GameStart.
Fecha y hora: 2025-10-13 22:20 UTC.
Instrucciones clave:
- GameStart es un Part::Feature (cono + base) con propiedades para yaw/pitch/roll/FOV/HeightOffset.
- Se identifica por la propiedad IsGameStartMarker.
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
"""GameStart utilities placeholder.

Descripcion rapida: creacion y consulta del objeto GameStart.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- GameStart debe ser un cono con base plana y propiedades para yaw/pitch/roll/FOV/HeightOffset.
- No incluir GameStart en exportacion de geometria.
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
- Mantener logs con prefijo [GAMEEXPORT].
"""

from __future__ import annotations

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
import math

from typing import Dict, List, Optional, Tuple

LOG_PREFIX = "[GAMEEXPORT] "
PROPERTIES = {
    "Yaw": ("App::PropertyFloat", 0.0, "GameStart", "Yaw (deg)"),
    "Pitch": ("App::PropertyFloat", 0.0, "GameStart", "Pitch (deg)"),
    "Roll": ("App::PropertyFloat", 0.0, "GameStart", "Roll (deg)"),
    "FieldOfView": ("App::PropertyFloat", 60.0, "GameStart", "Field of view (deg)"),
    "HeightOffset": ("App::PropertyFloat", 1.6, "GameStart", "Camera height offset (meters)"),
    "IsGameStartMarker": ("App::PropertyBool", True, "GameStart", "Internal marker for GameStart"),
}


def _generate_unique_name(doc, base: str = "GameStart") -> str:
    existing = {obj.Name for obj in getattr(doc, "Objects", [])}
    candidate = base
    index = 1
    while candidate in existing:
        candidate = f"{base}{index}"
        index += 1
    return candidate


def ensure_gamestart(doc, label: str = "GameStart"):
    """Create the GameStart marker if it does not exist."""
    FreeCAD = __import__("FreeCAD")
    Part = __import__("Part")

    existing = find_gamestart(doc, label)
    if existing:
        FreeCAD.Console.PrintMessage(LOG_PREFIX + f"GameStart already present: {existing.Name}\n")
        return existing

    if doc is None:
        FreeCAD.Console.PrintError(LOG_PREFIX + "Cannot create GameStart without an active document\n")
        return None

    try:
        name = doc.getUniqueObjectName("GameStart")
    except AttributeError:
        name = _generate_unique_name(doc, "GameStart")

    obj = doc.addObject("Part::Feature", name)
    obj.Label = label

    cone_height = 800.0
    cone_radius = 200.0
    base_height = 40.0
    base_radius = 260.0

    base = Part.makeCylinder(base_radius, base_height * 0.5, FreeCAD.Vector(0, 0, -base_height * 0.5))
    cone = Part.makeCone(0.0, cone_radius, cone_height, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    obj.Shape = Part.Compound([base, cone])

    for prop, (ptype, default, group, docstring) in PROPERTIES.items():
        if prop not in obj.PropertiesList:
            obj.addProperty(ptype, prop, group, docstring)
        setattr(obj, prop, default)

    # Convert legacy millimeter offsets (>= 20) to meters.
    try:
        if getattr(obj, "HeightOffset", 1.6) > 20.0:
            obj.HeightOffset = float(obj.HeightOffset) / 1000.0
    except Exception:
        pass

    obj.setEditorMode("IsGameStartMarker", 1)

    if hasattr(obj, "ViewObject"):
        obj.ViewObject.ShapeColor = (1.0, 0.4, 0.0)
        obj.ViewObject.Transparency = 40
        obj.ViewObject.DisplayMode = "Flat Lines"

    doc.recompute()
    FreeCAD.Console.PrintMessage(LOG_PREFIX + f"GameStart created: {obj.Name}\n")
    return obj


def find_gamestart(doc, label: str = "GameStart"):
    """Return the GameStart object if present."""
    if doc is None:
        return None

    for obj in doc.Objects:
        if getattr(obj, "IsGameStartMarker", False):
            return obj
    # Fallback by label
    for obj in doc.Objects:
        if obj.Label == label:
            return obj
    return None


def _compose_rotation(obj) -> Tuple[float, float, float, float]:
    """Return axis-angle (rad) from placement + user yaw/pitch/roll."""
    FreeCAD = __import__("FreeCAD")

    yaw = float(getattr(obj, "Yaw", 0.0))
    pitch = float(getattr(obj, "Pitch", 0.0))
    roll = float(getattr(obj, "Roll", 0.0))

    yaw_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), yaw)
    pitch_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), pitch)
    roll_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), roll)

    placement_rot = getattr(obj.Placement, "Rotation", FreeCAD.Rotation())
    final_rot = placement_rot.multiply(yaw_rot).multiply(pitch_rot).multiply(roll_rot)

    axis = final_rot.Axis
    angle_deg = final_rot.Angle
    if axis.Length == 0 or abs(angle_deg) < 1e-6:
        axis = FreeCAD.Vector(0, 1, 0)
        angle_rad = 0.0
    else:
        axis.normalize()
        angle_rad = math.radians(angle_deg)

    return axis.x, axis.y, axis.z, angle_rad


def get_metadata(obj) -> Optional[Dict[str, object]]:
    """Extract placement and configuration from the GameStart object."""
    if obj is None:
        return None

    FreeCAD = __import__("FreeCAD")

    placement = obj.Placement
    height_offset_m = float(getattr(obj, "HeightOffset", 1.6))
    if height_offset_m > 20.0:
        height_offset_m = height_offset_m / 1000.0
    height_offset_mm = height_offset_m * 1000.0

    base_vec = getattr(placement, "Base", FreeCAD.Vector(0, 0, 0))
    position_mm = (
        float(base_vec.x),
        float(base_vec.y),
        float(base_vec.z + height_offset_mm),
    )

    axis_angle = _compose_rotation(obj)
    raw_fov = getattr(obj, "FieldOfView", None)
    if raw_fov is None and hasattr(obj, "FOV"):
        raw_fov = getattr(obj, "FOV", 60.0)
    if raw_fov is None:
        raw_fov = 60.0
    fov_deg = float(raw_fov)

    description = getattr(obj, "Label", "") or getattr(obj, "Name", "") or "GameStart"
    return {
        "position_mm": position_mm,
        "orientation": axis_angle,
        "fov_rad": math.radians(fov_deg),
        "description": description.replace('"', "'"),
    }


__all__: List[str] = ["ensure_gamestart", "find_gamestart", "get_metadata"]
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
from typing import List


def ensure_gamestart(doc, label: str = "GameStart"):
    """Placeholder for GameStart creation."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] ensure_gamestart called for {label}\n")
    return None


def find_gamestart(doc, label: str = "GameStart"):
    """Placeholder for locating GameStart."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] find_gamestart called for {label}\n")
    return None


__all__: List[str] = ["ensure_gamestart", "find_gamestart"]
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
