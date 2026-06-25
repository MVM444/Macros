from pathlib import Path
path = Path('Macros-de-Freecad/ElectricCR/electriccr/features/objeto_toma_uno.py')
text = path.read_text(encoding='utf-8')
old = "    obj.addProperty(\"App::PropertyString\", \"RecursoProto2D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto3D\", \"Internal\", \"\")\n\n        self.initialized = True\n"
new = "    obj.addProperty(\"App::PropertyString\", \"RecursoProto2D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto3D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"KeyRegistro\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"IfcType\", \"Internal\", \"\")\n\n        self.initialized = True\n"
if old not in text:
    raise SystemExit('pattern not found when adding properties')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
