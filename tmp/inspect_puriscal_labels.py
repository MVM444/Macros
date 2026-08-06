import FreeCAD as App

path = r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Versión 2.FCStd"
doc = App.openDocument(path)
group = doc.getObject("Etiquetas")
print("GROUP", group, len(group.Group) if group else None)
for obj in list(group.Group if group else [])[:100]:
    values = []
    for prop in obj.PropertiesList:
        if prop.lower() in ("text", "string", "labeltext", "contents", "label", "layer", "placement") or "text" in prop.lower():
            try:
                values.append((prop, repr(getattr(obj, prop))))
            except Exception as exc:
                values.append((prop, "ERROR:" + str(exc)))
    print("OBJ", obj.TypeId, obj.Name, repr(obj.Label), values)
App.closeDocument(doc.Name)
