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


def icon_for_macro(dirname: str, filename: str) -> str:
    """Resolve icon for a specific macro by naming convention or header hint.

    Priority:
    1) icons/<dirname>/<base>.svg|png
    2) icons/<base>.svg|png
    3) '# Icon: name.svg' header hint inside macro
    4) ""
    """
    base = os.path.splitext(filename)[0]
    # 1) subdir icon
    for candidate in (f"{base}.svg", f"{base}.png"):
        p = os.path.join(ICONS_DIR, dirname, candidate)
        if os.path.exists(p):
            return p
    # 2) root icon
    root = icon_path(base)
    if root:
        return root
    # 3) header hint
    try:
        macro_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)), dirname, filename)
        with open(macro_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i in range(12):
                line = f.readline()
                if not line:
                    break
                if line.strip().lower().startswith('# icon:'):
                    name = line.split(':', 1)[1].strip()
                    p = icon_path(name)
                    if p:
                        return p
                    # also try subdir
                    p2 = os.path.join(ICONS_DIR, dirname, name)
                    if os.path.exists(p2):
                        return p2
                    break
    except Exception:
        pass
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

    def _sanitize_id(text: str) -> str:
        # Build a safe command id: letters, digits, underscore
        import re
        base = os.path.splitext(text)[0]
        base = re.sub(r"[^0-9A-Za-z_]+", "_", base)
        base = re.sub(r"_+", "_", base).strip("_")
        if not base:
            base = "Macro"
        return base

    def _cmd_id(prefix: str, name: str, macro_path: str, icon_path_str: str) -> str:
        try:
            mt = os.path.getmtime(macro_path) if os.path.exists(macro_path) else 0
            it = os.path.getmtime(icon_path_str) if icon_path_str and os.path.exists(icon_path_str) else 0
            ver = int(max(mt, it))
        except Exception:
            ver = 0
        return f"ElectricCR_{prefix}_{_sanitize_id(name)}_{ver}"

    def _register_dir_group(title: str, dirname: str, prefix: str, icon_name: str = ""):
        dir_path = os.path.join(repo_root, dirname)
        if not os.path.isdir(dir_path):
            return
        group_icon = icon_path(icon_name) if icon_name else ""
        cmd_ids = []
        # include both .FCMacro and .py
        for name in sorted(os.listdir(dir_path)):
            if name.lower().endswith((".fcmacro", ".py")):
                macro_path = os.path.join(dir_path, name)
                # Skip Windows metadata
                if os.path.basename(name).lower() == "desktop.ini":
                    continue
                label = os.path.splitext(name)[0]
                # try per-macro icon
                per_icon = icon_for_macro(dirname, name) or group_icon
                cmd_id = _cmd_id(prefix, name, macro_path, per_icon)
                cmd = register_macro_command(cmd_id, macro_path, label, icon=per_icon)
                if cmd:
                    cmd_ids.append(cmd)
        if cmd_ids:
            groups.append((title, cmd_ids))

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
        groups.append(("Tomacorrientes", toma_cmds))

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
        groups.append(("Conectar", con_cmds))

    # Otras carpetas (excluyendo Programación, Respaldos y Xcluidos)
    _register_dir_group("Áreas", "Areas", prefix="Areas")
    _register_dir_group("Iluminación", "Iluminación", prefix="Iluminacion")
    _register_dir_group("Objetos", "Objetos", prefix="Objetos")

    return groups
