"""GameEngineExportWB GUI bootstrap

Descripcion rapida: registro del workbench Game Engine Export WB y comando principal.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Registrar comandos sin cargar modulos pesados hasta ser necesarios.
- Mantener cadenas tecnicas en ASCII.
- Todos los logs deben usar prefijo [GAMEEXPORT].
- Priorizar comentarios claros para futuras ampliaciones.
"""

import FreeCAD
import FreeCADGui

from .commands import cmd_open_panel


class GameEngineExportWorkbench(FreeCADGui.Workbench):
    """Workbench definition for Game Engine Export WB."""

    MenuText = "Game Engine Export WB"
    ToolTip = "Export FreeCAD scenes to Castle Game Engine"
    Icon = FreeCAD.getHomePath() + "Mod/GameEngineExportWB/resources/icons/gameexport.svg"

    def Initialize(self):  # noqa: N802 (FreeCAD naming)
        """Register command and set up menus and toolbars."""
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Initializing workbench menus\n")
        FreeCADGui.addCommand(cmd_open_panel.CommandClass().CommandName, cmd_open_panel.CommandClass())
        self.appendToolbar("Game Engine Export", [cmd_open_panel.CommandClass().CommandName])
        self.appendMenu("Game Engine Export", [cmd_open_panel.CommandClass().CommandName])

    def Activated(self):  # noqa: N802
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Workbench activated\n")

    def Deactivated(self):  # noqa: N802
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Workbench deactivated\n")


FreeCADGui.addWorkbench(GameEngineExportWorkbench())
