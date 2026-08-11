import json
import os

import FreeCAD as App
import Draft


def sloped_faces(shape):
    result = []
    for index, face in enumerate(shape.Faces, 1):
        try:
            u1, u2, v1, v2 = face.ParameterRange
            normal = face.normalAt((u1 + u2) * 0.5, (v1 + v2) * 0.5)
            nz = abs(float(normal.z))
        except Exception:
            continue
        if 1e-5 < nz < 0.99999:
            box = face.BoundBox
            result.append(
                {
                    "index": index,
                    "normal": [round(normal.x, 6), round(normal.y, 6), round(normal.z, 6)],
                    "bbox": [
                        round(box.XMin, 3),
                        round(box.YMin, 3),
                        round(box.ZMin, 3),
                        round(box.XMax, 3),
                        round(box.YMax, 3),
                        round(box.ZMax, 3),
                    ],
                    "area": round(float(face.Area), 3),
                }
            )
    return result


def summary(label, wall):
    sloped = sloped_faces(wall.Shape)
    print(
        "FA_FACE_DIAG",
        json.dumps(
            {
                "label": label,
                "valid": bool(wall.Shape.isValid()),
                "volume": float(wall.Shape.Volume),
                "faces": len(wall.Shape.Faces),
                "sloped_count": len(sloped),
                "sloped": sloped[:30],
            }
        ),
    )


doc = App.openDocument(os.environ["FA_DIAG_SOURCE"])
doc.recompute()
wall = next(obj for obj in doc.Objects if Draft.getType(obj) == "Wall")
openings = [
    obj
    for obj in doc.Objects
    if str(getattr(obj, "IfcType", "") or "") in ("Door", "Window")
]
summary("hosted", wall)
for obj in openings:
    obj.Hosts = []
wall.touch()
doc.recompute()
summary("detached_all_openings", wall)
App.closeDocument(doc.Name)
