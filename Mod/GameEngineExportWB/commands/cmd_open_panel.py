"""Command to open the Game Engine Export panel.

Descripcion rapida: comando principal para mostrar la interfaz del workbench.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Mantener logs con prefijo [GAMEEXPORT].
- No ejecutar logica pesada aqui, solo abrir TaskPanel.
- Asegurar compatibilidad ASCII.
"""

import FreeCAD
import FreeCADGui

from ..ui import panel_scene


class CommandClass:
    """FreeCAD command wrapper for the TaskPanel."""

    CommandName = "GameEngineExport_Open"

    def GetResources(self):  # noqa: N802 (FreeCAD API)
        """Return metadata for menus and toolbars."""
        return {
            "MenuText": "Game Engine Export",
            "ToolTip": "Open the Game Engine Export panel",
            "Pixmap": "Mod/GameEngineExportWB/resources/icons/gameexport.svg",
        }

    def Activated(self):  # noqa: N802
        """Show the TaskPanel when the command runs."""
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Opening TaskPanel\n")
        FreeCADGui.Control.showDialog(panel_scene.TaskPanel())

    def IsActive(self):  # noqa: N802
        """Enable the command only when a document is open."""
        return FreeCAD.ActiveDocument is not None
