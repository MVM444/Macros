<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
"""Lights management helpers for Game Engine Export WB.

Descripcion rapida: gestionar objetos marcados como PointLight y producir datos de exportacion.
Fecha y hora: 2025-10-14 13:30 UTC.
Instrucciones clave:
- Utiliza propiedades del objeto para marcar luminarias persistentes.
- Provee funciones para convertir la seleccion en un conjunto de luces de escena.
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
"""Lights management placeholder for Game Engine Export WB.

Descripcion rapida: gestion de marcadores PointLight y datos asociados.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Mapear seleccion a objetos marcados como luces de escena.
- Preparar datos para insertar PointLight y SpotLight en X3D.
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

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

LOG_PREFIX = "[GAMEEXPORT] "
LIGHT_FLAG = "IsGameExportLight"
INTENSITY_PROP = "GameExportLightIntensity"
COLOR_PROP = "GameExportLightColor"
RADIUS_PROP = "GameExportLightRadius"
DEFAULT_INTENSITY = 1.2
DEFAULT_RADIUS = 12.0  # metros


@dataclass
class PointLightData:
    """Container for point light export data."""

    name: str
    label: str
    position_mm: tuple[float, float, float]
    intensity: float
    color_rgb: tuple[float, float, float]
    radius: float


def _ensure_light_properties(obj) -> None:
    """Ensure the FreeCAD object has the required GameExport properties."""
    if not hasattr(obj, "addProperty"):
        return
    if LIGHT_FLAG not in getattr(obj, "PropertiesList", []):
        obj.addProperty("App::PropertyBool", LIGHT_FLAG, "GameEngineExport", "Mark object as scene light")
    if INTENSITY_PROP not in getattr(obj, "PropertiesList", []):
        obj.addProperty("App::PropertyFloat", INTENSITY_PROP, "GameEngineExport", "PointLight intensity (0-5)")
        setattr(obj, INTENSITY_PROP, DEFAULT_INTENSITY)
    if COLOR_PROP not in getattr(obj, "PropertiesList", []):
        obj.addProperty("App::PropertyString", COLOR_PROP, "GameEngineExport", "PointLight RGB color (0-1 comma separated)")
        setattr(obj, COLOR_PROP, "1.0,1.0,1.0")
    if RADIUS_PROP not in getattr(obj, "PropertiesList", []):
        obj.addProperty("App::PropertyFloat", RADIUS_PROP, "GameEngineExport", "PointLight radius (meters)")
        setattr(obj, RADIUS_PROP, DEFAULT_RADIUS)


def _set_color_property(obj, color_rgb: tuple[float, float, float]) -> None:
    r, g, b = [max(0.0, min(1.0, float(c))) for c in color_rgb]
    setattr(obj, COLOR_PROP, f"{r:.4f},{g:.4f},{b:.4f}")


def _get_color_from_property(obj) -> tuple[float, float, float]:
    raw = getattr(obj, COLOR_PROP, "") or ""
    try:
        parts = [float(x) for x in raw.split(",")]
        if len(parts) == 3:
            return tuple(max(0.0, min(1.0, v)) for v in parts)
    except Exception:
        pass
    if hasattr(obj, "ViewObject"):
        try:
            vr, vg, vb = obj.ViewObject.ShapeColor[:3]
            return tuple(max(0.0, min(1.0, float(c))) for c in (vr, vg, vb))
        except Exception:
            pass
    return 1.0, 1.0, 1.0


def _get_position_mm(obj) -> tuple[float, float, float]:
    placement = getattr(obj, "Placement", None)
    if placement is not None:
        base = getattr(placement, "Base", None)
        if base is not None:
            return float(base.x), float(base.y), float(base.z)
    # fallback to bounding box center if available
    shape = getattr(obj, "Shape", None)
    if shape and hasattr(shape, "BoundBox") and not shape.isNull():
        bb = shape.BoundBox
        return float(bb.Center.x), float(bb.Center.y), float(bb.Center.z)
    return 0.0, 0.0, 0.0


def get_light_properties(obj) -> Dict[str, object]:
    """Return a snapshot of configurable light properties for a single object."""
    _ensure_light_properties(obj)
    intensity = float(getattr(obj, INTENSITY_PROP, DEFAULT_INTENSITY))
    intensity = max(0.0, min(5.0, intensity))
    radius = float(getattr(obj, RADIUS_PROP, DEFAULT_RADIUS))
    radius = max(0.1, radius)
    color = _get_color_from_property(obj)
    return {
        "intensity": intensity,
        "radius": radius,
        "color": color,
    }


def set_light_properties(
    doc,
    objects: Sequence[object],
    intensity: Optional[float] = None,
    radius: Optional[float] = None,
    color: Optional[Iterable[float]] = None,
) -> List[str]:
    """Apply light properties to the given objects and return their names."""
    if doc is None or not objects:
        return []
    updated = []
    color_tuple = None
    if color is not None:
        try:
            c = [float(v) for v in color]
            if len(c) == 3:
                color_tuple = tuple(max(0.0, min(1.0, v)) for v in c)
        except Exception:
            color_tuple = None
    for obj in objects:
        if obj is None or obj.Document != doc:
            continue
        _ensure_light_properties(obj)
        if intensity is not None:
            setattr(obj, INTENSITY_PROP, max(0.0, min(5.0, float(intensity))))
        if radius is not None:
            setattr(obj, RADIUS_PROP, max(0.1, float(radius)))
        if color_tuple is not None:
            _set_color_property(obj, color_tuple)
        updated.append(obj.Name)
    return updated


def list_point_lights(doc) -> List[object]:
    """Return all objects in the document flagged as scene lights."""
    if doc is None:
        return []
    results = []
    for obj in getattr(doc, "Objects", []):
        if getattr(obj, LIGHT_FLAG, False):
            results.append(obj)
    return results


def tag_selection_as_light(doc, selection: Sequence[object]) -> List[str]:
    """Mark the provided objects as point lights."""
    FreeCAD = __import__("FreeCAD")
    if doc is None or not selection:
        return []
    tagged = []
    for obj in selection:
        if obj is None or obj.Document != doc:
            continue
        _ensure_light_properties(obj)
        setattr(obj, LIGHT_FLAG, True)
        if getattr(obj, INTENSITY_PROP, 0.0) <= 0.0:
            setattr(obj, INTENSITY_PROP, DEFAULT_INTENSITY)
        _set_color_property(obj, _get_color_from_property(obj))
        tagged.append(obj.Name)
    if tagged:
        FreeCAD.Console.PrintMessage(LOG_PREFIX + f"Tagged as lights: {', '.join(tagged)}\n")
    return tagged


def untag_selection_as_light(doc, selection: Sequence[object]) -> List[str]:
    """Remove the light flag from the provided objects."""
    FreeCAD = __import__("FreeCAD")
    if doc is None or not selection:
        return []
    removed = []
    for obj in selection:
        if obj is None or obj.Document != doc:
            continue
        _ensure_light_properties(obj)
        setattr(obj, LIGHT_FLAG, False)
        removed.append(obj.Name)
    if removed:
        FreeCAD.Console.PrintMessage(LOG_PREFIX + f"Un-tagged lights: {', '.join(removed)}\n")
    return removed


def apply_light_names(doc, names: Iterable[str]) -> None:
    """Synchronise the light flag based on a list of object names."""
    desired = set(names or [])
    current = set()
    for obj in getattr(doc, "Objects", []):
        if getattr(obj, LIGHT_FLAG, False):
            current.add(obj.Name)
    # Unset objects that should no longer be lights
    for obj in getattr(doc, "Objects", []):
        if getattr(obj, LIGHT_FLAG, False) and obj.Name not in desired:
            setattr(obj, LIGHT_FLAG, False)
    # Tag desired
    for obj in getattr(doc, "Objects", []):
        if obj.Name in desired:
            _ensure_light_properties(obj)
            setattr(obj, LIGHT_FLAG, True)


def gather_point_light_data(doc, names: Iterable[str] | None = None) -> List[PointLightData]:
    """Return export-ready data for point lights."""
    if doc is None:
        return []
    allowed = set(names) if names is not None else None
    data: List[PointLightData] = []
    for obj in getattr(doc, "Objects", []):
        if not getattr(obj, LIGHT_FLAG, False):
            continue
        if allowed is not None and obj.Name not in allowed and obj.Label not in allowed:
            continue
        _ensure_light_properties(obj)
        props = get_light_properties(obj)
        intensity = props["intensity"]
        radius = props["radius"]
        color = props["color"]
        position = _get_position_mm(obj)
        data.append(
            PointLightData(
                name=obj.Name,
                label=getattr(obj, "Label", obj.Name),
                position_mm=position,
                intensity=intensity,
                color_rgb=color,
                radius=radius,
            )
        )
    return data


__all__: List[str] = [
    "PointLightData",
    "list_point_lights",
    "tag_selection_as_light",
    "untag_selection_as_light",
    "apply_light_names",
    "set_light_properties",
    "get_light_properties",
    "gather_point_light_data",
]
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


def list_point_lights(doc) -> List[object]:
    """Return placeholders for point light objects."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] list_point_lights placeholder\n")
    return []


def tag_selection_as_light(doc, selection):
    """Placeholder to tag current selection as a light."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] tag_selection_as_light placeholder\n")


def untag_selection_as_light(doc, selection):
    """Placeholder to remove light tag from selection."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] untag_selection_as_light placeholder\n")


__all__: List[str] = ["list_point_lights", "tag_selection_as_light", "untag_selection_as_light"]
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
