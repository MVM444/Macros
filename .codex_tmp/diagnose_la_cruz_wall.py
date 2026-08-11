import json
import os

import FreeCAD as App
import Draft


def shape_stats(shape):
    return {
        "is_null": bool(shape.isNull()),
        "is_valid": bool(shape.isValid()),
        "is_closed": bool(shape.isClosed()),
        "shape_type": str(shape.ShapeType),
        "volume": float(shape.Volume),
        "area": float(shape.Area),
        "solids": len(shape.Solids),
        "shells": len(shape.Shells),
        "faces": len(shape.Faces),
        "edges": len(shape.Edges),
        "vertices": len(shape.Vertexes),
        "bbox": [
            float(shape.BoundBox.XMin),
            float(shape.BoundBox.YMin),
            float(shape.BoundBox.ZMin),
            float(shape.BoundBox.XMax),
            float(shape.BoundBox.YMax),
            float(shape.BoundBox.ZMax),
        ],
    }


def main():
    path = os.environ["FA_DIAG_SOURCE"]
    doc = App.openDocument(path)
    doc.recompute()
    walls = [obj for obj in doc.Objects if Draft.getType(obj) == "Wall"]
    openings = [
        obj
        for obj in doc.Objects
        if str(getattr(obj, "IfcType", "") or "") in ("Door", "Window")
    ]
    print("FA_DIAG_DOC", json.dumps({"path": path, "objects": len(doc.Objects), "walls": len(walls), "openings": len(openings)}))
    for wall in walls:
        data = shape_stats(wall.Shape)
        data.update(
            {
                "name": wall.Name,
                "label": wall.Label,
                "width": float(wall.Width),
                "height": float(wall.Height),
                "base": getattr(getattr(wall, "Base", None), "Name", ""),
                "additions": [obj.Name for obj in list(getattr(wall, "Additions", []) or [])],
                "subtractions": [obj.Name for obj in list(getattr(wall, "Subtractions", []) or [])],
            }
        )
        print("FA_DIAG_WALL", json.dumps(data))
        invalid_solids = [index for index, solid in enumerate(wall.Shape.Solids, 1) if not solid.isValid()]
        invalid_faces = [index for index, face in enumerate(wall.Shape.Faces, 1) if not face.isValid()]
        print("FA_DIAG_WALL_INVALID", json.dumps({"invalid_solids": invalid_solids, "invalid_faces": invalid_faces}))
    opening_invalid = []
    cut_invalid = []
    for obj in openings:
        if not obj.Shape.isValid():
            opening_invalid.append(obj.Name)
        try:
            host = list(getattr(obj, "Hosts", []) or [None])[0]
            cut = obj.Proxy.getSubVolume(obj, host=host)
            if cut.isNull() or not cut.isValid():
                cut_invalid.append(obj.Name)
        except Exception as exc:
            cut_invalid.append("%s:%s" % (obj.Name, exc))
    print("FA_DIAG_OPENINGS", json.dumps({"invalid_shapes": opening_invalid, "invalid_cuts": cut_invalid}))
    App.closeDocument(doc.Name)


main()
