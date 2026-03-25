"""Lights management placeholder for Game Engine Export WB.

Descripcion rapida: gestion de marcadores PointLight y datos asociados.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Mapear seleccion a objetos marcados como luces de escena.
- Preparar datos para insertar PointLight y SpotLight en X3D.
- Mantener logs con prefijo [GAMEEXPORT].
"""

from __future__ import annotations

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
