import json
import os

import FreeCAD as App


doc = App.openDocument(os.environ["FA_LIST_SOURCE"])
sketch = doc.getObject("FA_GridWallTrace")
placement = sketch.getGlobalPlacement()
for index, geometry in enumerate(sketch.Geometry):
    if not hasattr(geometry, "StartPoint") or not hasattr(geometry, "EndPoint"):
        continue
    first = placement.multVec(geometry.StartPoint)
    second = placement.multVec(geometry.EndPoint)
    if max(first.x, second.x) < 9000 or min(first.x, second.x) > 16500:
        continue
    if max(first.y, second.y) < 6500 or min(first.y, second.y) > 13500:
        continue
    print(
        "FA_SEGMENT",
        json.dumps(
            {
                "index": index,
                "x1": first.x,
                "y1": first.y,
                "x2": second.x,
                "y2": second.y,
            }
        ),
    )
App.closeDocument(doc.Name)
