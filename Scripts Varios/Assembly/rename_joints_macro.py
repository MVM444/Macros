# Qt compatibility for FreeCAD 1.x (PySide6) and older builds.
def _ensure_qt_compat():
    import sys
    import types

    QtCore = QtGui = QtWidgets = None
    binding_name = None

    for candidate in ("PySide6", "PySide2", "PySide"):
        try:
            if candidate == "PySide":
                from PySide import QtCore as _QtCore, QtGui as _QtGui
                _QtWidgets = _QtGui
            else:
                module = __import__(candidate, fromlist=["QtCore", "QtGui", "QtWidgets"])
                _QtCore = module.QtCore
                _QtGui = module.QtGui
                _QtWidgets = module.QtWidgets
            QtCore, QtGui, QtWidgets = _QtCore, _QtGui, _QtWidgets
            binding_name = candidate
            break
        except Exception:
            continue

    if QtCore is None:
        return

    qtgui_compat = types.ModuleType("QtGui")
    qtgui_compat.__dict__.update(getattr(QtGui, "__dict__", {}))
    qtgui_compat.__dict__.update(getattr(QtWidgets, "__dict__", {}))

    qtsvg_compat = None
    for module_name in ("QtSvg", "QtSvgWidgets"):
        try:
            module = __import__(binding_name, fromlist=[module_name])
            qt_module = getattr(module, module_name)
        except Exception:
            continue
        if qtsvg_compat is None:
            qtsvg_compat = types.ModuleType("QtSvg")
        qtsvg_compat.__dict__.update(getattr(qt_module, "__dict__", {}))

    qtuitools_compat = None
    try:
        module = __import__(binding_name, fromlist=["QtUiTools"])
        qtuitools_compat = module.QtUiTools
    except Exception:
        pass

    for package_name in ("PySide2", "PySide"):
        package = sys.modules.get(package_name)
        if package is None:
            package = types.ModuleType(package_name)
            sys.modules[package_name] = package
        package.QtCore = QtCore
        package.QtGui = qtgui_compat
        package.QtWidgets = QtWidgets
        sys.modules[package_name + ".QtCore"] = QtCore
        sys.modules[package_name + ".QtGui"] = qtgui_compat
        sys.modules[package_name + ".QtWidgets"] = QtWidgets
        if qtsvg_compat is not None:
            package.QtSvg = qtsvg_compat
            sys.modules[package_name + ".QtSvg"] = qtsvg_compat
        if qtuitools_compat is not None:
            package.QtUiTools = qtuitools_compat
            sys.modules[package_name + ".QtUiTools"] = qtuitools_compat


_ensure_qt_compat()

# ==========================================================
# Macro: Rename_Joints_Assembly_102
# Fecha: 2025-01-26
# FreeCAD: 1.0.2
# Workbench: Assembly (integrado)
#
# Descripcion:
# Renombra el Label de las joints usando:
#   <JointType>_<Ref1>_<Ref2>
#
# Reglas:
# - Usa el formato real de Reference en Assembly 1.0.2
# - Renombra SOLO el Label (no el Name)
# - Puede renombrar todas o solo las seleccionadas
# - Usa marca interna RJ_Renamed para no repetir
# - Si Label contiene _ERROR_ se permite reintentar
# - Depuracion detallada en consola
# ==========================================================

import FreeCAD
import FreeCADGui
from PySide import QtGui

# ----------------------------------------------------------
# Debug helpers
# ----------------------------------------------------------

def dbg(msg):
    FreeCAD.Console.PrintMessage("[RenameJoints] " + str(msg) + "\n")

def dbg_err(msg):
    FreeCAD.Console.PrintError("[RenameJoints][ERROR] " + str(msg) + "\n")

# ----------------------------------------------------------
# Utils
# ----------------------------------------------------------

def sanitize(txt):
    try:
        s = str(txt)
    except Exception:
        s = "NONE"
    s = s.strip().replace(" ", "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s

def get_doc_object_label(obj_name):
    doc = FreeCAD.ActiveDocument
    if not doc:
        return sanitize(obj_name)
    obj = doc.getObject(obj_name)
    if obj:
        return sanitize(obj.Label)
    return sanitize(obj_name)

# ----------------------------------------------------------
# Reference parser (Assembly 1.0.2 REAL FORMAT)
# ----------------------------------------------------------

def get_reference_name(ref, ref_tag="Ref"):
    """
    Assembly 1.0.2 format:
    ref = (AssemblyObject, ["Obj.Sub", "Obj.Sub"])
    """
    dbg(ref_tag + " raw: " + str(ref))

    try:
        if not ref:
            return "NONE"

        if isinstance(ref, tuple) and len(ref) == 2:
            tokens = ref[1]
            if isinstance(tokens, list) and len(tokens) > 0:
                token = str(tokens[0])          # "Obj.Sub.Sub"
                obj_name = token.split(".")[0]  # "Obj"
                dbg(ref_tag + " token: " + token + " -> obj: " + obj_name)
                return get_doc_object_label(obj_name)

        dbg(ref_tag + " formato no reconocido")
        return "ERROR"

    except Exception as e:
        dbg_err(ref_tag + " error parseando: " + str(e))
        return "ERROR"

# ----------------------------------------------------------
# Get joints
# ----------------------------------------------------------

def get_joints(rename_all):
    doc = FreeCAD.ActiveDocument
    if not doc:
        dbg_err("No hay documento activo")
        return []

    joints = []

    if rename_all:
        dbg("Buscando todas las joints del documento")
        for obj in doc.Objects:
            if hasattr(obj, "Reference1") and hasattr(obj, "Reference2"):
                joints.append(obj)
    else:
        dbg("Buscando joints seleccionadas")
        sel = FreeCADGui.Selection.getSelection()
        for obj in sel:
            if hasattr(obj, "Reference1") and hasattr(obj, "Reference2"):
                joints.append(obj)

    dbg("Joints encontradas: " + str(len(joints)))
    return joints

# ----------------------------------------------------------
# Rename logic
# ----------------------------------------------------------

def rename_joints(rename_all=True):
    dbg("======================================")
    dbg("Inicio de renombrado de joints")
    dbg("Modo rename_all = " + str(rename_all))

    joints = get_joints(rename_all)
    if not joints:
        dbg("No hay joints para procesar")
        return

    for joint in joints:
        try:
            dbg("--------------------------------------")
            dbg("Procesando joint Name: " + str(joint.Name))
            dbg("Label antes: " + str(joint.Label))

            # Crear marca interna si no existe
            if not hasattr(joint, "RJ_Renamed"):
                joint.addProperty(
                    "App::PropertyBool",
                    "RJ_Renamed",
                    "RenameJoints",
                    "Renamed by macro"
                )
                joint.RJ_Renamed = False
                dbg("Propiedad RJ_Renamed creada")

            # Saltar si ya fue renombrada correctamente
            if joint.RJ_Renamed and "_ERROR_" not in joint.Label:
                dbg("Se omite (RJ_Renamed=True)")
                continue

            # Tipo de joint
            if hasattr(joint, "JointType"):
                joint_type = str(joint.JointType)
                dbg("JointType property: " + joint_type)
            else:
                tid = str(getattr(joint, "TypeId", "Joint"))
                joint_type = tid.split("::")[-1]
                dbg("JointType desde TypeId: " + joint_type)

            joint_type = sanitize(joint_type)
            if not joint_type:
                joint_type = "Joint"

            # References
            ref1_name = get_reference_name(joint.Reference1, "Reference1")
            ref2_name = get_reference_name(joint.Reference2, "Reference2")

            dbg("Referencia1 name: " + ref1_name)
            dbg("Referencia2 name: " + ref2_name)

            # Build label
            new_label = sanitize(joint_type + "_" + ref1_name + "_" + ref2_name)
            dbg("Nuevo Label: " + new_label)

            joint.Label = new_label
            joint.RJ_Renamed = True

            dbg("Renombrada correctamente")

        except Exception as e:
            dbg_err("Fallo procesando joint: " + str(e))

    FreeCAD.ActiveDocument.recompute()
    dbg("Renombrado finalizado")
    dbg("======================================")

# ----------------------------------------------------------
# UI
# ----------------------------------------------------------

def show_dialog():
    dlg = QtGui.QMessageBox()
    dlg.setWindowTitle("Rename Joints - Assembly 1.0.2")
    dlg.setText("Seleccione el modo de renombrado")

    btn_all = dlg.addButton("Todas las joints", QtGui.QMessageBox.AcceptRole)
    btn_sel = dlg.addButton("Solo seleccionadas", QtGui.QMessageBox.ActionRole)
    dlg.addButton("Cancelar", QtGui.QMessageBox.RejectRole)

    dlg.exec_()

    if dlg.clickedButton() == btn_all:
        rename_joints(True)
    elif dlg.clickedButton() == btn_sel:
        rename_joints(False)
    else:
        dbg("Operacion cancelada por el usuario")

# ----------------------------------------------------------
# Entry point
# ----------------------------------------------------------

show_dialog()
