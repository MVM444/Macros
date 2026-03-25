<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
"""X3D exporter helpers for Game Engine Export WB.

Descripcion rapida: exportar via FreeCADGui y decorar la escena con escala
mm->m y rotacion -90 en X.
Fecha y hora: 2025-10-13 21:30 UTC.
Instrucciones clave:
- Mantener logs con prefijo [GAMEEXPORT].
- Insertar Background, NavigationInfo y Transform envolvente.
- Preservar DOCTYPE si existe en el archivo original.
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
"""X3D exporter placeholder for Game Engine Export WB.

Descripcion rapida: modulacion de exportacion y decoracion X3D.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Implementar FreeCADGui.export y decoracion de X3D manteniendo escala 0.001 y rotacion -90 X.
- Insertar Background, NavigationInfo, luces y Viewpoint segun especificacion.
- Excluir GameStart de la geometria exportada.
- Mantener logs con prefijo [GAMEEXPORT].
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
"""

from __future__ import annotations

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List, Optional

SCALE_VECTOR = "0.001 0.001 0.001"
ROTATION_VECTOR = "1 0 0 -1.57079632679"
TRANSFORM_DEF = "FreeCAD_mm_to_m"
LOG_PREFIX = "[GAMEEXPORT] "


def export_to_x3d(
    objects: Iterable[object],
    output_path: Path,
    gamestart_meta: Optional[Dict[str, object]] = None,
    lighting_cfg: Optional[Dict[str, object]] = None,
) -> Path:
    """Export the given objects and decorate the X3D file."""
    FreeCAD = __import__("FreeCAD")
    FreeCADGui = __import__("FreeCADGui")

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    object_list = [obj for obj in objects if obj is not None]
    if not object_list:
        raise ValueError("No objects provided for export")

    FreeCAD.Console.PrintMessage(
        LOG_PREFIX + f"Exporting {len(object_list)} objects to {out_path}\n"
    )
    FreeCADGui.export(object_list, str(out_path))

    decorate_x3d(out_path, gamestart_meta, lighting_cfg)
    return out_path


def decorate_x3d(
    path: Path,
    gamestart_meta: Optional[Dict[str, object]] = None,
    lighting_cfg: Optional[Dict[str, object]] = None,
) -> None:
    """Post-process the X3D file to add scale/rotation and basic scene nodes."""
    FreeCAD = __import__("FreeCAD")

    path = Path(path)
    if not path.exists():
        FreeCAD.Console.PrintError(LOG_PREFIX + f"decorate_x3d missing file: {path}\n")
        return

    original_text = path.read_text(encoding="utf-8")
    doctype_line = ""
    for line in original_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("<!DOCTYPE"):
            doctype_line = stripped
            break

    try:
        tree = ET.ElementTree(ET.fromstring(original_text))
    except ET.ParseError as exc:
        FreeCAD.Console.PrintError(LOG_PREFIX + f"Failed to parse X3D: {exc}\n")
        return

    root = tree.getroot()
    namespace = ""
    if root.tag.startswith("{"):
        namespace = root.tag.split("}", 1)[0][1:]

    def q(tag: str) -> str:
        return f"{{{namespace}}}{tag}" if namespace else tag

    scene = root.find(q("Scene"))
    if scene is None:
        FreeCAD.Console.PrintError(LOG_PREFIX + "Scene node not found in X3D\n")
        return

    _ensure_background(scene, q)
    _ensure_navigation(scene, q)
    transform = _wrap_with_transform(scene, q)
    if gamestart_meta:
        _insert_viewpoint(scene, q, gamestart_meta)
    if lighting_cfg:
        global_cfg = lighting_cfg.get("global") if isinstance(lighting_cfg, dict) else None
        point_cfg = lighting_cfg.get("point_lights") if isinstance(lighting_cfg, dict) else None
        if global_cfg:
            _insert_directional_light(scene, q, global_cfg)
        if point_cfg:
            _insert_point_lights(scene, q, point_cfg)

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tree.write(tmp_path, encoding="utf-8", xml_declaration=True)
    rewritten = tmp_path.read_text(encoding="utf-8").splitlines()
    tmp_path.unlink(missing_ok=True)

    if doctype_line:
        if len(rewritten) >= 2:
            rewritten.insert(1, doctype_line)
        else:
            rewritten.append(doctype_line)

    rebuilt = "\n".join(rewritten)
    if original_text.endswith("\n"):
        rebuilt += "\n"

    path.write_text(rebuilt, encoding="utf-8")
    FreeCAD.Console.PrintMessage(LOG_PREFIX + f"decorate_x3d applied to {path}\n")


def _ensure_background(scene, q) -> None:
    """Insert a Background node if absent."""
    has_background = any(child.tag == q("Background") for child in scene)
    if not has_background:
        background = ET.Element(q("Background"), {"skyColor": "0.05 0.08 0.15"})
        scene.insert(0, background)


def _ensure_navigation(scene, q) -> None:
    """Insert a NavigationInfo node if absent."""
    has_navigation = any(child.tag == q("NavigationInfo") for child in scene)
    if not has_navigation:
        nav = ET.Element(
            q("NavigationInfo"),
            {
                "avatarSize": "0.25 1.6 0.75",
                "speed": "2",
                "headlight": "false",
                "type": '"WALK" "ANY"',
            },
        )
        insert_index = 1 if scene and scene[0].tag == q("Background") else 0
        scene.insert(insert_index, nav)


def _wrap_with_transform(scene, q):
    """Wrap the scene geometry inside a Transform with scale/rotation."""
    transform = None
    for child in scene:
        if child.tag == q("Transform") and child.attrib.get("DEF") == TRANSFORM_DEF:
            transform = child
            break

    if transform is None:
        transform = ET.Element(
            q("Transform"),
            {
                "DEF": TRANSFORM_DEF,
                "scale": SCALE_VECTOR,
                "rotation": ROTATION_VECTOR,
            },
        )
    else:
        transform.clear()  # remove children to repopulate
        transform.attrib["DEF"] = TRANSFORM_DEF
        transform.attrib["scale"] = SCALE_VECTOR
        transform.attrib["rotation"] = ROTATION_VECTOR

    preserved_tags = {q("Background"), q("NavigationInfo")}
    geometry_children = []
    for child in list(scene):
        if child.tag in preserved_tags:
            continue
        if child is transform:
            scene.remove(child)
            continue
        scene.remove(child)
        geometry_children.append(child)

    for child in geometry_children:
        transform.append(child)

    # Ensure transform is appended after preserved nodes
    scene.append(transform)
    return transform


def _insert_viewpoint(scene, q, meta: Dict[str, object]) -> None:
    """Insert or replace the Viewpoint based on GameStart metadata."""
    FreeCAD = __import__("FreeCAD")

    if not meta:
        return

    position_mm = meta.get("position_mm")
    orientation = meta.get("orientation")
    fov_rad = float(meta.get("fov_rad", math.radians(60.0)))
    description = meta.get("description", "GameStart")

    if position_mm is None or orientation is None:
        return

    transform_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)

    pos_vec = FreeCAD.Vector(*position_mm)
    pos_rot = transform_rot.multVec(pos_vec)
    position_m = (pos_rot.x * 0.001, pos_rot.y * 0.001, pos_rot.z * 0.001)

    axis_vec = FreeCAD.Vector(*orientation[:3])
    angle_rad = float(orientation[3])
    if axis_vec.Length == 0 or abs(angle_rad) < 1e-8:
        view_rot = FreeCAD.Rotation()
    else:
        view_rot = FreeCAD.Rotation(axis_vec, math.degrees(angle_rad))

    final_rot = transform_rot.multiply(view_rot)
    final_axis = final_rot.Axis
    if final_axis.Length == 0:
        final_axis = FreeCAD.Vector(0, 1, 0)
    else:
        final_axis.normalize()
    final_angle_rad = math.radians(final_rot.Angle)

    def_name = f"{description}_VP".replace(" ", "_")
    viewpoint_attrs = {
        "DEF": def_name,
        "description": description,
        "position": f"{position_m[0]:.6f} {position_m[1]:.6f} {position_m[2]:.6f}",
        "orientation": f"{final_axis.x:.6f} {final_axis.y:.6f} {final_axis.z:.6f} {final_angle_rad:.6f}",
        "fieldOfView": f"{fov_rad:.6f}",
        "jump": "true",
        "centerOfRotation": f"{position_m[0]:.6f} {position_m[1]:.6f} {position_m[2]:.6f}",
    }

    for child in list(scene):
        if child.tag == q("Viewpoint") and child.attrib.get("DEF") == viewpoint_attrs["DEF"]:
            scene.remove(child)

    insert_index = 0
    for idx, child in enumerate(scene):
        if child.tag in {q("Background"), q("NavigationInfo")}:
            insert_index = idx + 1

    viewpoint = ET.Element(q("Viewpoint"), viewpoint_attrs)
    scene.insert(insert_index, viewpoint)


def _insert_directional_light(scene, q, config: Dict[str, object]) -> None:
    FreeCAD = __import__("FreeCAD")

    if not config or not config.get("enabled", False):
        return

    yaw = float(config.get("yaw", 0.0))
    pitch = float(config.get("pitch", 0.0))
    intensity = max(0.0, min(5.0, float(config.get("intensity", 1.0))))
    color = config.get("color", (1.0, 1.0, 1.0))
    if isinstance(color, (list, tuple)) and len(color) == 3:
        color_tuple = tuple(max(0.0, min(1.0, float(c))) for c in color)
    else:
        color_tuple = (1.0, 1.0, 1.0)

    rot_global = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)
    yaw_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), yaw)
    pitch_rot = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), pitch)
    base_dir = FreeCAD.Vector(0, -1, 0)
    direction = pitch_rot.multiply(yaw_rot).multVec(base_dir)
    direction = rot_global.multVec(direction)
    if direction.Length == 0:
        direction = FreeCAD.Vector(0, -1, -1)
    try:
        direction.normalize()
    except Exception:
        direction = FreeCAD.Vector(0, -1, -1)
        direction.normalize()

    direction_str = f"{direction.x:.6f} {direction.y:.6f} {direction.z:.6f}"
    color_str = f"{color_tuple[0]:.4f} {color_tuple[1]:.4f} {color_tuple[2]:.4f}"

    # Remove previous global light if present
    for child in list(scene):
        if child.tag == q("DirectionalLight") and child.attrib.get("DEF") == "GameExport_GlobalLight":
            scene.remove(child)

    attrs = {
        "DEF": "GameExport_GlobalLight",
        "direction": direction_str,
        "intensity": f"{intensity:.4f}",
        "color": color_str,
    }
    insert_index = 0
    for idx, child in enumerate(scene):
        if child.tag in {q("Background"), q("NavigationInfo"), q("Viewpoint")}:
            insert_index = idx + 1
    scene.insert(insert_index, ET.Element(q("DirectionalLight"), attrs))


def _insert_point_lights(scene, q, entries: Iterable[Dict[str, object]]) -> None:
    FreeCAD = __import__("FreeCAD")

    to_remove = []
    for child in list(scene):
        if child.tag == q("PointLight") and child.attrib.get("DEF", "").endswith("_Light"):
            to_remove.append(child)
        elif child.tag == q("Transform"):
            if any(
                grand.tag == q("PointLight") and grand.attrib.get("DEF", "").endswith("_Light")
                for grand in list(child)
            ):
                to_remove.append(child)
    for node in to_remove:
        scene.remove(node)

    rot_global = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)

    insert_index = len(scene)
    for idx, child in enumerate(scene):
        if child.tag == q("Transform") and child.attrib.get("DEF") == TRANSFORM_DEF:
            insert_index = idx + 1

    for entry in entries:
        position_mm = entry.get("position_mm")
        if position_mm is None:
            continue
        pos_vec = FreeCAD.Vector(*position_mm)
        pos_rot = rot_global.multVec(pos_vec)
        position_m = (pos_rot.x * 0.001, pos_rot.y * 0.001, pos_rot.z * 0.001)
        location_str = f"{position_m[0]:.6f} {position_m[1]:.6f} {position_m[2]:.6f}"

        color = entry.get("color", (1.0, 1.0, 1.0))
        if isinstance(color, (list, tuple)) and len(color) == 3:
            color_tuple = tuple(max(0.0, min(1.0, float(c))) for c in color)
        else:
            color_tuple = (1.0, 1.0, 1.0)
        color_str = f"{color_tuple[0]:.4f} {color_tuple[1]:.4f} {color_tuple[2]:.4f}"

        intensity = max(0.0, min(5.0, float(entry.get("intensity", 1.0))))
        radius = max(0.1, float(entry.get("radius", 10.0)))

        raw_name = str(entry.get("name", "PointLight"))
        safe_name = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in raw_name) or "PointLight"
        light_attrs = {
            "DEF": f"{safe_name}_Light",
            "color": color_str,
            "intensity": f"{intensity:.4f}",
            "radius": f"{radius:.4f}",
            "location": location_str,
            "attenuation": "1 0 0",
        }
        scene.insert(insert_index, ET.Element(q("PointLight"), light_attrs))
        insert_index += 1
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
from pathlib import Path
from typing import Iterable, List


def export_to_x3d(objects: Iterable[object], output_path: Path) -> Path:
    """Placeholder for export routine."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage(
        f"[GAMEEXPORT] export_to_x3d called with {len(list(objects))} objects -> {output_path}\n"
    )
    return output_path


def decorate_x3d(path: Path) -> None:
    """Placeholder for X3D post processing."""
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] decorate_x3d placeholder for {path}\n")
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


__all__: List[str] = ["export_to_x3d", "decorate_x3d"]
