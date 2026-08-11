import json
import os

import FreeCAD as App


doc = App.openDocument(os.environ["FA_LIST_SOURCE"])
doc.recompute()
for obj in doc.Objects:
    shape = getattr(obj, "Shape", None)
    box = None
    if shape is not None and not shape.isNull():
        bb = shape.BoundBox
        box = [bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax]
    print(
        "FA_OBJECT",
        json.dumps(
            {
                "name": obj.Name,
                "label": obj.Label,
                "type": obj.TypeId,
                "role": str(getattr(obj, "FA_Role", "") or ""),
                "kind": str(getattr(obj, "FA_CenterlineKind", "") or ""),
                "geometry_count": len(list(getattr(obj, "Geometry", []) or [])),
                "bbox": box,
            }
        ),
    )
App.closeDocument(doc.Name)
