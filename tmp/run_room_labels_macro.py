import FreeCAD as App

model = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
macro = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\RecopilarRotulosRecintos.FCMacro"
doc = App.openDocument(model)
namespace = {"__file__": macro, "__name__": "__main__"}
exec(compile(open(macro, "rb").read(), macro, "exec"), namespace)
sheet = doc.getObject("Spreadsheet_Rotulos_Recintos")
print("SHEET", sheet is not None, sheet.Label if sheet else None)
print("ROWS", [(row, sheet.get("A%d" % row), sheet.get("B%d" % row), sheet.get("C%d" % row)) for row in range(2, 27)])
doc.recompute()
doc.save()
App.closeDocument(doc.Name)
