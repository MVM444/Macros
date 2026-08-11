import os
import sys

import FreeCAD as App
import FreeCADGui as Gui


SOURCE = os.environ["FA_CAPTURE_SOURCE"]
OUTPUT = os.environ["FA_CAPTURE_OUTPUT"]


def main():
    doc = App.openDocument(SOURCE)
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().setAnimationEnabled(False)
    Gui.activeDocument().activeView().fitAll(0.90)
    Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(OUTPUT, 1800, 1200, "White")
    if not os.path.isfile(OUTPUT) or os.path.getsize(OUTPUT) == 0:
        raise RuntimeError("FreeCAD no genero la captura")
    print("FA_CAPTURE_OK " + OUTPUT)
    App.closeDocument(doc.Name)
    Gui.getMainWindow().close()


main()
