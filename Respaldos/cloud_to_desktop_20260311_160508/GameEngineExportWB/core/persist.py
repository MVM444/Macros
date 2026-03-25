"""Persistence helpers for Game Engine Export WB.

Descripcion rapida: manejo de ParamGet y sidecar JSON.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Guardar configuracion global en User parameter:BaseApp/Preferences/GameEngineExport.
- Manejar sidecar <DocStem>.gee.json en la carpeta del documento.
- Mantener logs con prefijo [GAMEEXPORT].
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


PREF_GROUP = "User parameter:BaseApp/Preferences/GameEngineExport"
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
LOG_PREFIX = "[GAMEEXPORT] "
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
=======
>>>>>>> theirs


def load_global_prefs(param_get) -> Dict[str, object]:
    """Placeholder for reading global preferences."""
    FreeCAD = __import__("FreeCAD")
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    FreeCAD.Console.PrintMessage(LOG_PREFIX + "load_global_prefs placeholder\n")
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] load_global_prefs placeholder\n")
>>>>>>> theirs
    return {}


def save_global_prefs(param_get, data: Dict[str, object]) -> None:
    """Placeholder for writing global preferences."""
    FreeCAD = __import__("FreeCAD")
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    FreeCAD.Console.PrintMessage(LOG_PREFIX + "save_global_prefs placeholder\n")
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] save_global_prefs placeholder\n")
>>>>>>> theirs


def load_sidecar(doc_path: Path) -> Dict[str, object]:
    """Read sidecar JSON if present."""
    FreeCAD = __import__("FreeCAD")
    sidecar = doc_path.with_suffix(".gee.json")
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    FreeCAD.Console.PrintMessage(LOG_PREFIX + f"load_sidecar checking {sidecar}\n")
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
=======
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] load_sidecar checking {sidecar}\n")
>>>>>>> theirs
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - placeholder handling
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
        FreeCAD.Console.PrintError(LOG_PREFIX + f"Failed to read sidecar: {exc}\n")
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
=======
        FreeCAD.Console.PrintError(f"[GAMEEXPORT] Failed to read sidecar: {exc}\n")
>>>>>>> theirs
        return {}


def save_sidecar(doc_path: Path, data: Dict[str, object]) -> Path:
    """Write sidecar JSON."""
    sidecar = doc_path.with_suffix(".gee.json")
    FreeCAD = __import__("FreeCAD")
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    try:
        payload = json.dumps(data, indent=2, sort_keys=True)
        sidecar.write_text(payload, encoding="utf-8")
        FreeCAD.Console.PrintMessage(LOG_PREFIX + f"Sidecar saved at {sidecar}\n")
    except Exception as exc:  # pragma: no cover - defensive
        FreeCAD.Console.PrintError(LOG_PREFIX + f"Failed to save sidecar: {exc}\n")
    return sidecar


__all__: List[str] = [
    "PREF_GROUP",
    "LOG_PREFIX",
    "load_global_prefs",
    "save_global_prefs",
    "load_sidecar",
    "save_sidecar",
]
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
    sidecar.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    FreeCAD.Console.PrintMessage(f"[GAMEEXPORT] Sidecar saved at {sidecar}\n")
    return sidecar


__all__: List[str] = ["PREF_GROUP", "load_global_prefs", "save_global_prefs", "load_sidecar", "save_sidecar"]
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
