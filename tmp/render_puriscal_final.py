import FreeCAD as App
import FreeCADGui as Gui

model = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
image = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.png"

doc = App.openDocument(model)
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(image, 1400, 1000, "Current")
print("RENDERED", image)
App.closeDocument(doc.Name)
Gui.getMainWindow().close()
