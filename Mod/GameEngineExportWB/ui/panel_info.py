"""Information tab for Game Engine Export WB.

Descripcion rapida: texto informativo bilingue.
Fecha y hora: 2025-10-13 13:54 UTC.
Instrucciones clave:
- Presentar reglas de exportacion resumidas.
- Proveer boton para copiar texto (placeholder sin funcionalidad avanzada).
"""

from PySide import QtCore, QtGui


INFO_TEXT = (
    "ES: El Workbench exporta escenas FreeCAD a X3D con escala 0.001, rotacion global -90 grados en X y Viewpoint desde GameStart.\n"
    "EN: The workbench exports FreeCAD scenes to X3D with 0.001 scale, global -90 deg X rotation and Viewpoint from GameStart.\n\n"
    "ES: Evita acentos y caracteres especiales en nombres y rutas. Requiere un piso para caminar.\n"
    "EN: Avoid accents and special characters in names and paths. Requires at least one floor for walking.\n\n"
    "ES: Usa la raiz para limitar la escena, la lista manual es opcional, GameStart define la camara inicial.\n"
    "EN: Use the root to limit the scene, manual list is optional, GameStart defines the initial camera.\n\n"
    "ES: Creditos: creado por el Ing. Marco Vinicio Mora Fallas con ayuda de ChatGPT (99.9%).\n"
    "EN: Credits: created by Ing. Marco Vinicio Mora Fallas with help from ChatGPT (99.9%)."
)


def build_info_tab():
    """Return the information QWidget."""
    tab = QtGui.QWidget()
    layout = QtGui.QVBoxLayout(tab)

    text = QtGui.QPlainTextEdit()
    text.setPlainText(INFO_TEXT)
    text.setReadOnly(True)
    layout.addWidget(text)

    btn_copy = QtGui.QPushButton("Copiar / Copy")
    btn_copy.setToolTip("ES: Copia todo el texto informativo.\nEN: Copies the full information text.")
    layout.addWidget(btn_copy)

    btn_copy.clicked.connect(lambda: _copy_to_clipboard(text.toPlainText()))

    layout.addStretch()
    return tab


def _copy_to_clipboard(value):
    """Copy text to clipboard (best effort)."""
    clipboard = QtGui.QApplication.clipboard()
    clipboard.setText(value, QtGui.QClipboard.Clipboard)
    clipboard.setText(value, QtGui.QClipboard.Selection)
    FreeCAD = __import__("FreeCAD")
    FreeCAD.Console.PrintMessage("[GAMEEXPORT] Info text copied\n")


__all__ = ["build_info_tab"]
