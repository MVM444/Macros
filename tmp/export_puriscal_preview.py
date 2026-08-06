import FreeCAD as App
import Mesh

model = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd"
out = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\tmp"
doc = App.openDocument(model)
for filename, names in (
    ("puriscal_wall.stl", ("Wall",)),
    ("puriscal_columns.stl", ("Structure",)),
    ("puriscal_slab.stl", ("Structure001",)),
    ("puriscal_terrain.stl", ("FA_TestTerrain",)),
):
    objects = [doc.getObject(name) for name in names if doc.getObject(name) is not None]
    Mesh.export(objects, out + "\\" + filename)
    print("EXPORTED", filename)
App.closeDocument(doc.Name)
