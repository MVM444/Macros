# -*- coding: utf-8 -*-
"""GUI smoke test for the global Programacion toolbar; never saves a document."""

import os
import sys
import traceback

import FreeCAD as App
import FreeCADGui as Gui


def qt_modules():
    from PySide6 import QtCore, QtWidgets
    return QtCore, QtWidgets


def run():
    root = App.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath", "").split(";")[0]
    folder = os.path.join(root, "Programación")
    if folder not in sys.path:
        sys.path.insert(0, folder)
    import programacion_toolbar

    controller = programacion_toolbar.install(folder)
    QtCore, QtWidgets = qt_modules()
    window = Gui.getMainWindow()
    expected = [item[0] for item in programacion_toolbar.MANIFEST]
    missing = [name for name in expected if name not in Gui.listCommands()]
    assert not missing, "missing commands: {}".format(missing)
    assert len([tb for tb in window.findChildren(QtWidgets.QToolBar) if tb.objectName() == "Programacion"]) == 1
    programacion_toolbar.install(folder)
    assert len([tb for tb in window.findChildren(QtWidgets.QToolBar) if tb.objectName() == "Programacion"]) == 1
    for workbench in ("PartWorkbench", "DraftWorkbench"):
        if workbench in Gui.listWorkbenches():
            Gui.activateWorkbench(workbench)
            QtWidgets.QApplication.processEvents()
            controller.ensure_visible()
            assert controller.toolbar.isVisible()
    doc = App.newDocument("ProgramacionToolbarSmoke")
    group = doc.addObject("App::DocumentObjectGroup", "GrupoPrueba")
    feature = doc.addObject("App::FeaturePython", "ObjetoPrueba")
    group.addObject(feature)
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(feature)
    Gui.runCommand("Programacion_SelectionSummary")
    Gui.runCommand("Programacion_PropertiesJSON")
    Gui.runCommand("Programacion_UIAudit")
    Gui.runCommand("Programacion_Capture3D")
    capture = getattr(window, "_programacion_coordinate_capture", None)
    assert capture is not None
    capture.stop("smoke test")
    App.closeDocument(doc.Name)
    print("PROGRAMACION_GUI_SMOKE=PASS")
    QtCore.QTimer.singleShot(0, QtWidgets.QApplication.instance().quit)


try:
    run()
except Exception:
    traceback.print_exc()
    QtCore, QtWidgets = qt_modules()
    print("PROGRAMACION_GUI_SMOKE=FAIL")
    QtCore.QTimer.singleShot(0, QtWidgets.QApplication.instance().quit)
    raise
