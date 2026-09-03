"""Prueba externa y no persistente de FreeCAD-HVAC en FreeCAD 1.1.3.

Este archivo no forma parte de FreeCAD-HVAC y no modifica su codigo fuente.
Se ejecuta como argumento de FreeCAD GUI, crea un documento temporal, prueba
la creacion de una red y una ruta minima, registra el resultado y cierra el
documento sin guardarlo.
"""

import json
import os
import traceback

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


RESULT_PATH = os.path.join(
    r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros",
    "Documentacion_organizacion",
    "Pruebas_FreeCAD_HVAC",
    "resultado_verificacion_2026-08-22.json",
)
DOCUMENT_NAME = "Codex_HVAC_Smoke_20260822"


def _active_workbench_name():
    wb = Gui.activeWorkbench()
    return wb.name() if wb else None


def _wait_for_deferred_gui_work(milliseconds=1200):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(milliseconds, loop.quit)
    if hasattr(loop, "exec"):
        loop.exec()
    else:
        loop.exec_()


def _object_summary(obj):
    proxy = getattr(obj, "Proxy", None)
    return {
        "name": obj.Name,
        "label": obj.Label,
        "type_id": obj.TypeId,
        "proxy_class": proxy.__class__.__name__ if proxy else None,
    }


def _write_result(result):
    with open(RESULT_PATH, "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)


def verify():
    result = {
        "test": "FreeCAD-HVAC GUI smoke test",
        "freecad_version": list(App.Version()),
        "user_data_dir": App.getUserAppDataDir(),
        "documents_before": sorted(App.listDocuments().keys()),
        "workbench_before": _active_workbench_name(),
        "workbench_hvac_present_before_activation": False,
        "workbench_hvac_activated": False,
        "commands": [],
        "missing_expected_commands": [],
        "hvac_toolbars": [],
        "hvac_menus": [],
        "network_created": False,
        "route_added": False,
        "route_length_mm": None,
        "segments_created": 0,
        "junctions_created": 0,
        "objects": [],
        "document_saved": False,
        "documents_after": [],
        "status": "ERROR",
        "error": None,
        "traceback": None,
    }

    expected_commands = [
        "HVAC_CreateDuctNetwork",
        "HVAC_ActivateDuctNetwork",
        "HVAC_ModifyDuctNetwork",
        "HVAC_EditNetworkTypeDefaults",
        "HVAC_CreateSketch",
        "HVAC_CreateLine",
        "HVAC_CreateSpline",
        "HVAC_CreateVirtualJunction",
        "HVAC_EditBaseObject",
        "HVAC_EditDuctDirections",
        "HVAC_EditType",
        "HVAC_EditPlacement",
        "HVAC_ResetTypesToDefaults",
    ]

    doc = None
    try:
        workbenches = Gui.listWorkbenches()
        result["workbench_names"] = sorted(workbenches.keys())
        result["workbench_hvac_present_before_activation"] = "HVAC" in workbenches
        if "HVAC" not in workbenches:
            raise RuntimeError("HVAC no aparece en Gui.listWorkbenches()")

        Gui.activateWorkbench("HVAC")
        QtWidgets.QApplication.processEvents()
        result["workbench_after_activation"] = _active_workbench_name()
        result["workbench_hvac_activated"] = result["workbench_after_activation"] == "HVAC"

        result["commands"] = sorted(
            command for command in Gui.listCommands() if command.startswith("HVAC_")
        )
        result["missing_expected_commands"] = sorted(
            set(expected_commands) - set(result["commands"])
        )

        main_window = Gui.getMainWindow()
        for toolbar in main_window.findChildren(QtWidgets.QToolBar):
            title = toolbar.windowTitle() or ""
            object_name = toolbar.objectName() or ""
            if "HVAC" in title.upper() or "HVAC" in object_name.upper():
                result["hvac_toolbars"].append(
                    {
                        "title": title,
                        "object_name": object_name,
                        "visible": toolbar.isVisible(),
                        "actions": [
                            action.text().replace("&", "")
                            for action in toolbar.actions()
                            if not action.isSeparator()
                        ],
                    }
                )
        for menu in main_window.findChildren(QtWidgets.QMenu):
            title = (menu.title() or "").replace("&", "")
            if title.strip().upper() == "HVAC":
                result["hvac_menus"].append(
                    {
                        "title": title,
                        "actions": [
                            action.text().replace("&", "")
                            for action in menu.actions()
                            if not action.isSeparator()
                        ],
                    }
                )

        doc = App.newDocument(DOCUMENT_NAME)
        Gui.runCommand("HVAC_CreateDuctNetwork")
        QtWidgets.QApplication.processEvents()

        from freecad.HVAC.utils import hvaclib

        networks = [obj for obj in doc.Objects if hvaclib.isDuctNetwork(obj)]
        if len(networks) != 1:
            raise RuntimeError(
                "Se esperaba una red HVAC y se encontraron {}".format(len(networks))
            )
        network = networks[0]
        result["network_created"] = True

        import Draft

        route = Draft.make_line(App.Vector(0, 0, 0), App.Vector(2000, 0, 0))
        result["route_added"] = bool(network.Proxy.addBaseObject(route))
        doc.recompute()
        _wait_for_deferred_gui_work()
        doc.recompute()

        result["route_length_mm"] = float(route.Shape.Length)
        segments = [obj for obj in doc.Objects if hvaclib.isDuctSegment(obj)]
        junctions = [obj for obj in doc.Objects if hvaclib.isDuctJunction(obj)]
        result["segments_created"] = len(segments)
        result["junctions_created"] = len(junctions)
        result["objects"] = [_object_summary(obj) for obj in doc.Objects]

        if not result["workbench_hvac_activated"]:
            raise RuntimeError("HVAC no quedo como Workbench activo")
        if result["missing_expected_commands"]:
            raise RuntimeError("Faltan comandos HVAC esperados")
        if not result["route_added"] or result["route_length_mm"] <= 0:
            raise RuntimeError("La ruta minima no se agrego correctamente")
        if result["segments_created"] < 1:
            raise RuntimeError("La ruta no genero ningun segmento de ducto")

        result["status"] = "OK"
    except Exception as exc:
        result["error"] = repr(exc)
        result["traceback"] = traceback.format_exc()
    finally:
        if doc is not None and doc.Name in App.listDocuments():
            App.closeDocument(doc.Name)
        result["documents_after"] = sorted(App.listDocuments().keys())
        _write_result(result)
        QtCore.QTimer.singleShot(750, Gui.getMainWindow().close)


QtCore.QTimer.singleShot(1500, verify)
