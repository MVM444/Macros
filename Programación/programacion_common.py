# -*- coding: utf-8 -*-
"""Shared read-only helpers for Programacion diagnostics.

Purpose: keep Qt, document metadata, hierarchy and clipboard handling consistent.
Usage: imported by macros stored directly in this directory.
Version: 1.0.0
Date: 2026-08-12 00:00 CST
"""

import os

import FreeCAD as App


PREFIX = "[PROGRAMACION]"


def qt_modules():
    for binding in ("PySide6", "PySide2", "PySide"):
        try:
            module = __import__(binding, fromlist=["QtCore", "QtGui", "QtWidgets"])
            core = module.QtCore
            gui = module.QtGui
            widgets = getattr(module, "QtWidgets", gui)
            return core, gui, widgets
        except Exception:
            continue
    raise RuntimeError("No compatible PySide binding found")


def info(tool, message):
    App.Console.PrintMessage("{}[{}] {}\n".format(PREFIX, tool, message))


def warning(tool, message):
    App.Console.PrintWarning("{}[{}][WARN] {}\n".format(PREFIX, tool, message))


def error(tool, message):
    App.Console.PrintError("{}[{}][ERROR] {}\n".format(PREFIX, tool, message))


def text(value, default=""):
    try:
        return str(value if value is not None else default)
    except Exception:
        return default


def clipboard_set(value):
    _core, _gui, widgets = qt_modules()
    app = widgets.QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication is unavailable")
    app.clipboard().setText(text(value))


def freecad_version():
    try:
        return ".".join(text(part) for part in App.Version()[:3])
    except Exception:
        return "unknown"


def document_metadata(doc=None):
    doc = doc or App.ActiveDocument
    if doc is None:
        return {"name": "", "label": "", "file": ""}
    filename = text(getattr(doc, "FileName", ""))
    return {
        "name": text(getattr(doc, "Name", "")),
        "label": text(getattr(doc, "Label", "")),
        "file": os.path.abspath(filename) if filename else "",
    }


def is_group(obj):
    try:
        return bool(obj.isDerivedFrom("App::DocumentObjectGroup") or obj.isDerivedFrom("App::Part"))
    except Exception:
        return hasattr(obj, "Group")


def parent_groups(obj):
    result = []
    for parent in list(getattr(obj, "InList", []) or []):
        try:
            if is_group(parent) and obj in list(getattr(parent, "Group", []) or []):
                result.append(parent)
        except Exception:
            continue
    return result


def hierarchy_paths(obj, branch=None):
    branch = set(branch or ())
    key = text(getattr(obj, "Name", "")) or "id:{}".format(id(obj))
    if key in branch:
        return [[obj]]
    branch.add(key)
    parents = parent_groups(obj)
    if not parents:
        return [[obj]]
    result = []
    for parent in parents:
        for path in hierarchy_paths(parent, branch):
            result.append(path + [obj])
    return result or [[obj]]


def path_text(obj):
    paths = []
    for path in hierarchy_paths(obj):
        paths.append(" / ".join(
            "{} [{}]".format(text(getattr(item, "Label", "")) or text(getattr(item, "Name", "")),
                             text(getattr(item, "Name", "")))
            for item in path
        ))
    return paths


def link_data(obj):
    type_id = text(getattr(obj, "TypeId", ""))
    linked = None
    try:
        linked = getattr(obj, "LinkedObject", None)
    except Exception:
        linked = None
    if linked is None:
        try:
            linked = obj.getLinkedObject(False)
        except Exception:
            linked = None
    return {
        "is_link": type_id == "App::Link" or linked is not None,
        "linked_name": text(getattr(linked, "Name", "")) if linked else "",
        "linked_label": text(getattr(linked, "Label", "")) if linked else "",
    }
