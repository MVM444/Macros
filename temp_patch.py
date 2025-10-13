from pathlib import Path
path = Path('Macros-de-Freecad/ElectricCR/electriccr/features/objeto_toma_uno.py')
text = path.read_text(encoding='utf-8')
old = "    obj.addProperty(\"App::PropertyString\", \"LabelProto3D\", \"Internal\", \"\").LabelProto3D = \"ProtoToma3D\"\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto2D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto3D\", \"Internal\", \"\")\n\n        self.initialized = True\n        log_i(f\"attach properties on {obj.Name}\")\n\n"
new = "    obj.addProperty(\"App::PropertyString\", \"LabelProto3D\", \"Internal\", \"\").LabelProto3D = \"ProtoToma3D\"\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto2D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"RecursoProto3D\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"KeyRegistro\", \"Internal\", \"\")\n    obj.addProperty(\"App::PropertyString\", \"IfcType\", \"Internal\", \"\")\n\n        self.initialized = True\n        log_i(f\"attach properties on {obj.Name}\")\n\n"
if old not in text:
    raise SystemExit('target not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
