import os

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore


SOURCE = os.environ["FA_CAPTURE_SOURCE"]
OUTPUT = os.environ["FA_CAPTURE_OUTPUT"]

doc = App.openDocument(SOURCE)
view = Gui.activeDocument().activeView()

if os.environ.get("FA_CAPTURE_DETACH_OPENINGS") == "1":
    for obj in doc.Objects:
        if str(getattr(obj, "IfcType", "") or "") in {"Door", "Window"}:
            obj.Hosts = []
    for obj in doc.Objects:
        if str(getattr(obj, "FA_Role", "") or "") == "wall":
            obj.touch()
    doc.recompute()


def close_freecad():
    App.closeDocument(doc.Name)
    Gui.getMainWindow().close()


def save_capture():
    Gui.updateGui()
    view.saveImage(OUTPUT, 1800, 1200, "White")
    if not os.path.isfile(OUTPUT) or os.path.getsize(OUTPUT) == 0:
        raise RuntimeError("FreeCAD no genero la captura isometrica")
    print("FA_ISOMETRIC_CAPTURE_OK " + OUTPUT)
    QtCore.QTimer.singleShot(250, close_freecad)


def prepare_view():
    if os.environ.get("FA_CAPTURE_BIM_ONLY") == "1":
        for obj in doc.Objects:
            obj.ViewObject.Visibility = False
        for obj in doc.Objects:
            role = str(getattr(obj, "FA_Role", "") or "")
            if role in {"wall", "column", "door", "window"}:
                obj.ViewObject.Visibility = True
    hidden_roles = {
        "axis_family",
        "centerlines",
        "door_base",
        "grid_clipped_lines",
        "window_base",
    }
    for obj in doc.Objects:
        role = str(getattr(obj, "FA_Role", "") or "")
        if obj.TypeId == "Sketcher::SketchObject" or role in hidden_roles:
            obj.ViewObject.Visibility = False
        if os.environ.get("FA_CAPTURE_HIDE_OPENINGS") == "1" and role in {"door", "window"}:
            obj.ViewObject.Visibility = False
    draw_style = os.environ.get("FA_CAPTURE_DRAW_STYLE", "Flat Lines")
    for obj in doc.Objects:
        if not obj.ViewObject.Visibility:
            continue
        try:
            obj.ViewObject.DisplayMode = draw_style
        except Exception:
            pass
    view.viewAxonometric()
    view.fitAll()
    if os.environ.get("FA_CAPTURE_FIX_CLIPPING") == "1":
        camera = view.getCameraNode()
        camera.nearDistance = 1.0
        camera.farDistance = 1000000.0
    Gui.updateGui()
    QtCore.QTimer.singleShot(1500, save_capture)


QtCore.QTimer.singleShot(1000, prepare_view)
