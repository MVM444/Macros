import os
import FreeCAD as App

doc = App.openDocument(os.environ["FA_CAPTURE_SOURCE"])
for obj in doc.Objects:
    shape = getattr(obj, "Shape", None)
    if shape is None or shape.isNull():
        continue
    box = shape.BoundBox
    role = getattr(obj, "FA_Role", "")
    if box.ZLength > 1.0 or role:
        print(
            "FA_BBOX",
            obj.Name,
            obj.TypeId,
            role,
            round(box.XLength, 2),
            round(box.YLength, 2),
            round(box.ZLength, 2),
        )
App.closeDocument(doc.Name)
