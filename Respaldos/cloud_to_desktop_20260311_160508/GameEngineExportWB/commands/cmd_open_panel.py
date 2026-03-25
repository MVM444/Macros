<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
"""Command to open the export TaskPanel.

Descripcion rapida: comando para seleccionar objetos y exportar a X3D.
Fecha y hora: 2025-10-13 19:00 UTC.
Instrucciones clave:
- Registrar logs con prefijo [GAMEEXPORT].
- Abrir el panel de exportacion cuando exista documento activo.
- Mantener cadenas ASCII.
"""

import os

import FreeCAD
import FreeCADGui

from ..ui import panel_export

ICON_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "gameexport.svg")
).replace(os.sep, "/")


class CommandClass:
    """FreeCAD command wrapper for the export TaskPanel."""

    CommandName = "GameEngineExport_Export"

    def GetResources(self):  # noqa: N802 (FreeCAD API)
        return {
            "MenuText": "Exportar X3D",
            "ToolTip": "Seleccionar objetos y exportar a X3D",
            "Pixmap": ICON_PATH,
        }

    def Activated(self):  # noqa: N802
        FreeCAD.Console.PrintMessage("[GAMEEXPORT] Opening export panel\n")
        FreeCADGui.Control.showDialog(panel_export.ExportTaskPanel())

    def IsActive(self):  # noqa: N802
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
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
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
        try:
            if hasattr(FreeCADGui.Control, "activeDialog") and FreeCADGui.Control.activeDialog():
                FreeCAD.Console.PrintMessage("[GAMEEXPORT] Closing previous active task dialog\n")
                FreeCADGui.Control.closeDialog()
        except Exception as exc:  # pragma: no cover - FreeCAD runtime safety
            FreeCAD.Console.PrintWarning(f"[GAMEEXPORT] Could not close active dialog: {exc}\n")
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
        FreeCADGui.Control.showDialog(panel_scene.TaskPanel())

    def IsActive(self):  # noqa: N802
        """Enable the command only when a document is open."""
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
        return FreeCAD.ActiveDocument is not None
