# -*- coding: utf-8 -*-
"""Global Programacion toolbar loader for FreeCAD 1.1.3.

Purpose: register stable commands from direct child macros only.
Usage: executed automatically by Mod/DevPathsBootstrap/InitGui.py.
Version: 1.0.0
Date: 2026-08-12 00:00 CST
"""

import os
import sys

import FreeCAD as App
import FreeCADGui as Gui

PREFIX = "[PROGRAMACION][TOOLBAR]"
TOOLBAR = "Programacion"
STATE = "_programacion_toolbar_controller"
MANIFEST = (
    ("Programacion_CopyLastMinute", "CopyReportLast1Min.FCMacro", "Copiar ultimo minuto", "Copia inmediatamente el ultimo minuto de reportes o FreeCAD.log."),
    ("Programacion_CaptureTreePrompt", "CapturarArbolYPrompt.FCMacro", "Capturar arbol y prompt", "Exporta el arbol y copia un prompt tecnico."),
    ("Programacion_SelectionSummary", "Copiar_Nombres_Seleccion.FCMacro", "Copiar resumen de seleccion", "Copia identidad, tipos, rutas y Links seleccionados."),
    ("Programacion_PropertiesJSON", "CopyObjectProperties.FCMacro", "Extraer propiedades del objeto", "Extrae las propiedades de los objetos seleccionados y las copia como JSON."),
    ("Programacion_UIAudit", "AuditarInterfazFreeCAD.FCMacro", "Auditar interfaz de FreeCAD", "Copia una auditoria read-only de la interfaz."),
    ("Programacion_Capture3D", "CapturarCoordenadas3D.FCMacro", "Capturar coordenadas 3D", "Captura un clic 3D y retira el callback."),
    ("Programacion_OpenFolders", "Abrir_Directorios_FreeCAD.FCMacro", "Abrir directorios recurrentes", "Abre destinos recurrentes desde un menu pequeno."),
    ("Programacion_OllamaAssistant", "Ollama_Asistente_Local.FCMacro", "Ollama Asistente Local", "Abre el asistente local Ollama existente para FreeCAD."),
)
ICON_OVERRIDES = {
    "Ollama_Asistente_Local.FCMacro": "ollama_llama_icon.svg",
}


def icon_for(folder, filename):
    icon_name = ICON_OVERRIDES.get(filename, os.path.splitext(filename)[0] + ".svg")
    icon = os.path.join(folder, icon_name)
    if not os.path.isfile(icon):
        icon = os.path.join(folder, "Programacion.svg")
    return icon


def log(message, error=False):
    target = App.Console.PrintError if error else App.Console.PrintMessage
    target("{} {}\n".format(PREFIX, message))


def qt_modules():
    for binding in ("PySide6", "PySide2", "PySide"):
        try:
            module = __import__(binding, fromlist=["QtCore", "QtGui", "QtWidgets"])
            return module.QtCore, module.QtGui, getattr(module, "QtWidgets", module.QtGui)
        except Exception:
            continue
    raise RuntimeError("No compatible PySide binding found")


class MacroCommand:
    def __init__(self, folder, filename, label, tooltip):
        self.path = os.path.join(folder, filename)
        self.icon = icon_for(folder, filename)
        self.label = label
        self.tooltip = tooltip

    def GetResources(self):
        return {"Pixmap": self.icon.replace(os.sep, "/"), "MenuText": self.label, "ToolTip": self.tooltip}

    def Activated(self):
        namespace = {"__file__": self.path, "__name__": "__main__"}
        folder = os.path.dirname(self.path)
        if folder not in sys.path:
            sys.path.insert(0, folder)
        try:
            with open(self.path, "r", encoding="utf-8-sig") as handle:
                code = compile(handle.read(), self.path, "exec")
            exec(code, namespace, namespace)
        except Exception as exc:
            log("Error en {}: {}".format(self.label, exc), True)
            raise

    def IsActive(self):
        return os.path.isfile(self.path)


class Controller:
    def __init__(self, folder):
        self.folder = folder
        self.actions = []
        self.toolbar = None
        self.timer = None
        self.install()

    def register_commands(self):
        for command, filename, label, tooltip in MANIFEST:
            path = os.path.join(self.folder, filename)
            if not os.path.isfile(path) or os.path.dirname(path) != self.folder:
                log("Omitido; archivo directo inexistente: " + filename, True)
                continue
            Gui.addCommand(command, MacroCommand(self.folder, filename, label, tooltip))
            log("Comando registrado: {} -> {}".format(command, filename))

    def build_toolbar(self):
        _core, _gui, widgets = qt_modules()
        window = Gui.getMainWindow()
        matches = [tb for tb in window.findChildren(widgets.QToolBar) if tb.objectName() == TOOLBAR]
        self.toolbar = matches[0] if matches else widgets.QToolBar(TOOLBAR, window)
        self.toolbar.setObjectName(TOOLBAR)
        self.toolbar.setWindowTitle(TOOLBAR)
        if not matches:
            window.addToolBar(self.toolbar)
        self.toolbar.clear()
        self.actions = []
        for command, filename, label, tooltip in MANIFEST:
            if not os.path.isfile(os.path.join(self.folder, filename)):
                continue
            action = self.toolbar.addAction(label)
            icon = icon_for(self.folder, filename)
            action.setIcon(_gui.QIcon(icon))
            action.setToolTip(tooltip)
            action.triggered.connect(lambda checked=False, name=command: Gui.runCommand(name))
            self.actions.append(action)
        self.toolbar.show()
        self.toolbar.setVisible(True)
        App.ParamGet("User parameter:BaseApp/Preferences/MainWindow/Toolbars").SetBool(TOOLBAR, True)
        log("Barra lista. Botones={}.".format(len(self.actions)))

    def ensure_visible(self):
        if self.toolbar is not None:
            self.toolbar.show()
            self.toolbar.setVisible(True)

    def install(self):
        self.register_commands()
        self.build_toolbar()
        core, _gui, _widgets = qt_modules()
        self.timer = core.QTimer(Gui.getMainWindow())
        self.timer.setInterval(1500)
        self.timer.timeout.connect(self.ensure_visible)
        self.timer.start()


def install(folder=None):
    folder = os.path.abspath(folder or os.path.dirname(__file__))
    window = Gui.getMainWindow()
    previous = getattr(window, STATE, None)
    if previous is not None:
        try:
            previous.folder = folder
            previous.register_commands()
            previous.build_toolbar()
            previous.ensure_visible()
            log("Instalacion existente actualizada; no se duplico la barra.")
            return previous
        except Exception:
            pass
    controller = Controller(folder)
    setattr(window, STATE, controller)
    return controller
