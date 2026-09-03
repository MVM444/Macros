"""FreeCAD 1.1.3 smoke test for the isolated Puriscal double BIM door."""

from __future__ import annotations

import json
import os

import FreeCAD as App


HERE = os.path.dirname(os.path.abspath(__file__))
PURISCAL_DIR = os.path.dirname(HERE)
MACRO_PATH = os.path.join(PURISCAL_DIR, "ElectricCR_PuertaDobleBIM_Puriscal_v001.FCMacro")
MACROS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PURISCAL_DIR)))
OUTPUT_DIR = os.path.join(MACROS_ROOT, ".codex_tmp")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "ElectricCR_PuertaDobleBIM_Puriscal_v001.FCStd")


def centers(shape):
    return [tuple(round(value, 6) for value in solid.CenterOfMass) for solid in shape.Solids]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MACRO_PATH, "r", encoding="utf-8-sig") as handle:
        source = handle.read()
    namespace = {"__file__": MACRO_PATH, "__name__": "__main__"}
    exec(compile(source, MACRO_PATH, "exec"), namespace, namespace)

    doc = namespace["created_document"]
    group = namespace["created_group"]
    profile = namespace["created_profile"]
    door = namespace["created_door"]
    doc.recompute()

    assert doc is App.ActiveDocument
    assert set(group.Group) == {profile, door}
    assert door.TypeId == "Part::FeaturePython"
    assert door.Proxy.__class__.__module__ == "ArchWindow"
    assert door.IfcType == "Door"
    assert abs(door.Width.Value - 2000.0) < 1e-6
    assert abs(door.Height.Value - 2100.0) < 1e-6
    assert door.Hosts == []
    assert door.Material is not None
    assert door.Material.Names == ["Frame", "Solid panel", "Glass panel"]
    assert [material.Label for material in door.Material.Materials] == [
        "Aluminio gris satinado",
        "Panel inferior gris",
        "Vidrio laminado 6 mm",
    ]
    assert tuple(round(value, 2) for value in door.Material.Materials[0].Color[:3]) == (
        0.62,
        0.64,
        0.66,
    )
    assert tuple(round(value, 2) for value in door.Material.Materials[2].Color[:3]) == (
        0.42,
        0.72,
        0.90,
    )
    assert int(door.Material.Materials[2].Transparency) == 70
    for material in door.Material.Materials:
        assert "DiffuseColor" in material.Material, material.Label
    assert "Transparency" in door.Material.Materials[2].Material
    if App.GuiUp and door.ViewObject:
        import ArchWindow

        ArchWindow.recolorize(door)
        unique_appearance = {
            (
                tuple(round(channel, 3) for channel in item.DiffuseColor),
                round(float(item.Transparency), 3),
            )
            for item in door.ViewObject.ShapeAppearance
        }
        assert len(unique_appearance) >= 3, unique_appearance
    assert door.Base is profile and door.Profile is profile
    assert profile.Owner is door
    assert len(profile.Shape.Wires) == 16
    assert len(profile.Shape.Edges) == 64
    assert len(door.WindowParts) == 65
    assert len(door.Shape.Solids) == 13
    assert door.SymbolPlan is True
    assert door.SymbolElevation is True
    assert "Opening" in door.PropertiesList

    motion = {}
    for opening in (0, 25, 50, 100, 0):
        door.Opening = opening
        doc.recompute()
        motion[str(opening)] = centers(door.Shape)
        assert len(door.Shape.Solids) == 13

    closed = motion["0"]
    door.Opening = 25
    doc.recompute()
    opened = centers(door.Shape)
    assert abs(opened[0][1] - closed[0][1]) < 1e-6
    left_delta = opened[1][1] - closed[1][1]
    right_delta = opened[7][1] - closed[7][1]
    assert abs(left_delta) > 1.0
    assert abs(right_delta) > 1.0
    # Opposite rotation modes around opposite exterior hinges make both leaves
    # swing toward the same side of the doorway.
    assert left_delta * right_delta > 0.0
    assert abs(abs(left_delta) - abs(right_delta)) < 1e-6
    for index in range(1, 7):
        assert (opened[index][1] - closed[index][1]) * left_delta > 0.0
    for index in range(7, 13):
        assert (opened[index][1] - closed[index][1]) * right_delta > 0.0

    door.Opening = 0
    doc.recompute()
    object_count = len(doc.Objects)
    component_count = len(door.WindowParts) // 5
    door_name = door.Name
    profile_name = profile.Name
    doc.saveAs(OUTPUT_PATH)
    App.closeDocument(doc.Name)

    reopened = App.openDocument(OUTPUT_PATH)
    reopened.recompute()
    restored_door = reopened.getObject(door_name)
    restored_profile = reopened.getObject(profile_name)
    assert restored_door is not None and restored_profile is not None
    assert restored_door.IfcType == "Door"
    assert restored_door.Base is restored_profile
    assert restored_profile.Owner is restored_door
    assert len(reopened.Objects) == object_count
    reopened.recompute()
    assert len(reopened.Objects) == object_count
    App.closeDocument(reopened.Name)

    report = {
        "output": OUTPUT_PATH,
        "objects": object_count,
        "components": component_count,
        "solids": len(closed),
        "left_delta_y_at_25": left_delta,
        "right_delta_y_at_25": right_delta,
        "persistence": "ok",
    }
    print("PUERTA_DOBLE_BIM_V001_SMOKE_OK", json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
