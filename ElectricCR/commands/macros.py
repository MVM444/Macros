# -*- coding: utf-8 -*-

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")


def icon_path(basename: str) -> str:
    for candidate in (f"{basename}.svg", f"{basename}.png", basename):
        path = os.path.join(ICONS_DIR, candidate)
        if os.path.exists(path):
            return path
    return ""


def _run_macro_file(macro_abspath: str):
    """Execute a .FCMacro (Python) file in the current FreeCAD session."""
    try:
        if not os.path.exists(macro_abspath):
            raise FileNotFoundError(macro_abspath)
        with open(macro_abspath, 'r', encoding='utf-8', errors='ignore') as f:
            src = f.read()
        code = compile(src, macro_abspath, 'exec')
        # Prepare a globals dict that resembles a macro execution context
        g = {
            '__name__': '__main__',
            '__file__': macro_abspath,
            'FreeCAD': App,
            'App': App,
            'FreeCADGui': Gui,
            'Gui': Gui,
            'os': os,
            'sys': sys,
        }
        cwd_prev = os.getcwd()
        try:
            os.chdir(os.path.dirname(macro_abspath))
            exec(code, g, g)
        finally:
            os.chdir(cwd_prev)
    except Exception as e:
        App.Console.PrintError(f"Error ejecutando macro: {macro_abspath}: {e}\n")


def register_macro_command(cmd_name: str, macro_path: str, menu_text: str, tooltip: str = "", icon: str = "") -> str:
    macro_abspath = os.path.abspath(macro_path)
    if not os.path.exists(macro_abspath):
        return ""

    class _MacroCmd:
        def GetResources(self):
            return {
                'Pixmap': icon or "",
                'MenuText': menu_text,
                'ToolTip': tooltip or menu_text,
            }

        def Activated(self):
            _run_macro_file(macro_abspath)

        def IsActive(self):
            return True

    Gui.addCommand(cmd_name, _MacroCmd())
    return cmd_name


def register_predefined_macros(base_dir: str):
    """Register selected macros from the repository and return toolbar groups.

    Returns: list of tuples (title, [command_names])
    """
    repo_root = os.path.abspath(os.path.join(base_dir, os.pardir))

    groups = []

    # Tomacorrientes group
    toma_icon = icon_path('tomacorriente')
    tomas = [
        ("ElectricCR_Toma_InsertarUno", os.path.join(repo_root, 'Tomacorrientes', 'InsertarTomacorriente.FCMacro'), "Insertar Tomacorriente"),
        ("ElectricCR_Toma_InsertarVarios", os.path.join(repo_root, 'Tomacorrientes', 'InsertarTomacorrientes.FCMacro'), "Insertar Tomacorrientes"),
        ("ElectricCR_Toma_MoverAGrupo", os.path.join(repo_root, 'Tomacorrientes', 'Mover_Tomacorrientes_a_grupo.FCMacro'), "Mover Tomacorrientes a grupo"),
        ("ElectricCR_Toma_Rotar", os.path.join(repo_root, 'Tomacorrientes', 'RotarTomacorriente.FCMacro'), "Rotar Tomacorriente"),
        ("ElectricCR_Toma_ContarExportar", os.path.join(repo_root, 'Tomacorrientes', 'contar_tomacorrientes_y_exportar.FCMacro'), "Contar y exportar Tomacorrientes"),
    ]
    toma_cmds = []
    for name, path, label in tomas:
        cmd = register_macro_command(name, path, label, icon=toma_icon)
        if cmd:
            toma_cmds.append(cmd)
    if toma_cmds:
        groups.append(("Electric • Tomacorrientes", toma_cmds))

    # Conectar group
    conectar = [
        ("ElectricCR_Conectar_en_C", os.path.join(repo_root, 'Conectar', 'Conectar_objetos_en_C.FCMacro'), "Conectar objetos en C"),
        ("ElectricCR_MedirRuta", os.path.join(repo_root, 'Conectar', 'medir_distancia_y_dibujar_ruta.FCMacro'), "Medir distancia y dibujar ruta"),
        ("ElectricCR_Conectar_Grupo", os.path.join(repo_root, 'Conectar', 'ConectarObjetosdeunGrupo.FCMacro'), "Conectar objetos de un grupo"),
        ("ElectricCR_Conectar_Bordes", os.path.join(repo_root, 'Conectar', 'conectar_objetos_por_bordes.FCMacro'), "Conectar por bordes"),
    ]
    con_cmds = []
    for name, path, label in conectar:
        cmd = register_macro_command(name, path, label, icon=icon_path('Rayo'))
        if cmd:
            con_cmds.append(cmd)
    if con_cmds:
        groups.append(("Electric • Conectar", con_cmds))

    return groups
