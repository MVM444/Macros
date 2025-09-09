# -*- coding: utf-8 -*-

import os
import FreeCAD as App
import FreeCADGui as Gui

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")

def icon_path(basename):
    candidates = [f"{basename}.svg", f"{basename}.png", basename]
    for candidate in candidates:
        path = os.path.join(ICONS_DIR, candidate)
        if os.path.exists(path):
            return path
    return ""


class InsertOutletCommand:
    def GetResources(self):
        return {
            'Pixmap': icon_path('tomacorriente'),
            'MenuText': 'Insertar Tomacorriente',
            'ToolTip': 'Inserta un tomacorriente en el modelo',
        }

    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            doc = App.newDocument()

        # Crear un objeto de tomacorriente (cilindro simple)
        outlet = doc.addObject("Part::Cylinder", "Tomacorriente")
        outlet.Radius = 5
        outlet.Height = 2

        # Posicionar el tomacorriente en el origen
        outlet.Placement.Base = App.Vector(0, 0, 0)

        doc.recompute()

    def IsActive(self):
        return True


COMMAND_NAME = 'ElectricCR_InsertOutlet'
Gui.addCommand(COMMAND_NAME, InsertOutletCommand())
