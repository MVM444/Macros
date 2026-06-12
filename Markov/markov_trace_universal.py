#!/usr/bin/env python

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

# markov_trace_universal.py
# Un solo archivo para:
# - Ejecutar un script Python y generar un grafo "Markov-like" de llamadas (DOT/PNG)
# - GUI Tk (standalone) o GUI Qt/PySide (cuando corre dentro de FreeCAD), o CLI
#
# Uso CLI:
#   python markov_trace_universal.py TU_SCRIPT.py [args...] --png
#   python markov_trace_universal.py --help
#
# Uso con GUI:
#   python markov_trace_universal.py --gui auto
#   (en FreeCAD, la GUI será Qt automáticamente)

import sys, os, runpy, argparse, subprocess
from collections import defaultdict

# ----------------- núcleo de trazado -----------------
_trans = defaultdict(int)
_last = [None]

def _qualname(frame):
    mod = frame.f_globals.get("__name__", "?")
    func = frame.f_code.co_name
    if func == "<module>":
        return f"{mod}.__module__"
    cls = None
    if "self" in frame.f_locals:
        try:
            cls = type(frame.f_locals["self"]).__name__
        except Exception:
            cls = None
    return f"{mod}.{cls+'.' if cls else ''}{func}"

def _tracer_factory(includes, excludes):
    includes = includes or []
    excludes = excludes or []
    def allowed(qname):
        mod = qname.split(".", 1)[0]
        if includes and not any(tok in mod for tok in includes): return False
        if excludes and any(tok in mod for tok in excludes): return False
        return True
    def tracer(frame, event, arg):
        try:
            if event == "call":
                cur = _qualname(frame)
                if not allowed(cur):
                    return tracer
                prev = _last[0]
                if prev is not None and allowed(prev):
                    _trans[(prev, cur)] += 1
                _last[0] = cur
            elif event in ("return","exception"):
                caller = frame.f_back
                _last[0] = _qualname(caller) if caller else None
        except Exception:
            pass
        return tracer
    return tracer

def _write_dot(out_path, mincount=1):
    by_src = defaultdict(int)
    for (src, dst), c in _trans.items():
        if c >= mincount: by_src[src] += c
    lines = ["digraph G {","  rankdir=LR;",'  node [shape=box, fontname="Arial"];']
    for (src, dst), c in _trans.items():
        if c < mincount: continue
        total = max(1, by_src[src]); p = c/total
        s = src.replace('"', r'\"'); d = dst.replace('"', r'\"')
        lines.append(f'  "{s}" -> "{d}" [label="{c} | {p:.2f}"];')
    lines.append("}")
    with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(lines))
    return out_path

def _has_graphviz():
    try:
        subprocess.run(["dot","-V"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except Exception:
        return False

def _dot_to_png(dot_path, png_path):
    try:
        subprocess.run(["dot","-Tpng", dot_path, "-o", png_path], check=True); return True
    except Exception:
        return False

def trace_and_export(target_script, script_args, outdir=None, includes=None, excludes=None, mincount=1, want_png=False):
    """Ejecuta el script objetivo bajo sys.settrace y exporta DOT/PNG."""
    _trans.clear(); _last[0] = None
    target_script = os.path.abspath(target_script)
    outdir = outdir or os.path.dirname(target_script)
    os.makedirs(outdir, exist_ok=True)
    dot_path = os.path.join(outdir, "markov.dot")
    png_path = os.path.join(outdir, "markov.png")

    tracer = _tracer_factory(includes, excludes)

    saved_argv = sys.argv[:]
    sys.argv = [target_script] + (script_args or [])
    try:
        sys.settrace(tracer)
        try:
            runpy.run_path(target_script, run_name="__main__")
        finally:
            sys.settrace(None)
    except SystemExit:
        pass
    finally:
        sys.argv = saved_argv

    _write_dot(dot_path, mincount=mincount)
    png_ok = False
    if want_png and _has_graphviz():
        png_ok = _dot_to_png(dot_path, png_path)
    return dot_path, (png_path if png_ok else None)

# ----------------- detección de entorno -----------------
def running_in_freecad():
    try:
        import FreeCAD  # noqa
        return True
    except Exception:
        return False

# ----------------- GUI Tk (standalone) -----------------
def launch_tk_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Markov Tracer (Tk GUI)")
            self.geometry("720x400")
            self.script = tk.StringVar()
            self.args   = tk.StringVar()
            self.outdir = None
            self.include = tk.StringVar()
            self.exclude = tk.StringVar()
            self.mincount = tk.IntVar(value=1)
            self.want_png = tk.BooleanVar(value=True)

            frm = ttk.Frame(self, padding=10); frm.pack(fill="both", expand=True)
            ttk.Label(frm, text="Script:").grid(row=0, column=0, sticky="w")
            ttk.Entry(frm, textvariable=self.script, width=60).grid(row=0, column=1, sticky="we")
            ttk.Button(frm, text="Examinar…", command=self._browse).grid(row=0, column=2, padx=5)

            ttk.Label(frm, text="Argumentos:").grid(row=1, column=0, sticky="w", pady=(6,0))
            ttk.Entry(frm, textvariable=self.args).grid(row=1, column=1, columnspan=2, sticky="we", pady=(6,0))

            ttk.Label(frm, text="Include (módulos, coma-sep):").grid(row=2, column=0, sticky="w", pady=(6,0))
            ttk.Entry(frm, textvariable=self.include).grid(row=2, column=1, columnspan=2, sticky="we", pady=(6,0))

            ttk.Label(frm, text="Exclude (módulos, coma-sep):").grid(row=3, column=0, sticky="w", pady=(6,0))
            ttk.Entry(frm, textvariable=self.exclude).grid(row=3, column=1, columnspan=2, sticky="we", pady=(6,0))

            options = ttk.Frame(frm); options.grid(row=4, column=0, columnspan=3, sticky="w", pady=(6,0))
            ttk.Checkbutton(options, text="Generar PNG (Graphviz)", variable=self.want_png).pack(side="left")
            ttk.Label(options, text="Min. conteo:").pack(side="left", padx=(12,4))
            ttk.Entry(options, textvariable=self.mincount, width=5).pack(side="left")

            btns = ttk.Frame(frm); btns.grid(row=5, column=0, columnspan=3, sticky="w", pady=(8,0))
            ttk.Button(btns, text="Trazar", command=self._run).pack(side="left")
            ttk.Button(btns, text="Abrir carpeta", command=self._open_out).pack(side="left", padx=8)

            self.log = tk.Text(frm, height=12, wrap="word"); self.log.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(8,0))
            frm.columnconfigure(1, weight=1); frm.rowconfigure(6, weight=1)

        def _browse(self):
            p = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("Todos", "*.*")])
            if p: self.script.set(p)

        def _open_out(self):
            if self.outdir and os.path.isdir(self.outdir):
                if sys.platform.startswith("win"): os.startfile(self.outdir)
                elif sys.platform == "darwin": subprocess.run(["open", self.outdir])
                else: subprocess.run(["xdg-open", self.outdir])

        def _run(self):
            s = self.script.get().strip()
            if not s or not os.path.isfile(s):
                messagebox.showerror("Error", "Selecciona un script .py válido."); return
            self.outdir = os.path.dirname(os.path.abspath(s))
            inc = [t.strip() for t in self.include.get().split(",") if t.strip()]
            exc = [t.strip() for t in self.exclude.get().split(",") if t.strip()]
            args = self.args.get().split()
            self._log(f"[INFO] Ejecutando {os.path.basename(s)} {' '.join(args)}")
            try:
                dot, png = trace_and_export(s, args, outdir=self.outdir,
                                            includes=inc, excludes=exc,
                                            mincount=max(1,int(self.mincount.get())),
                                            want_png=self.want_png.get())
                self._log(f"[OK] DOT: {dot}")
                if png: self._log(f"[OK] PNG: {png}")
                else:   self._log("[INFO] Si quieres PNG, instala Graphviz y activa la casilla.")
            except Exception as ex:
                self._log(f"[ERROR] {ex}")

        def _log(self, msg):
            self.log.insert("end", msg + "\n"); self.log.see("end")

    App().mainloop()

# ----------------- GUI Qt (PySide) para FreeCAD o PySide instalable -----------------
def launch_qt_gui():
    # Intenta PySide6, si no PySide2 (FreeCAD 0.20/0.21 usaba 2; FreeCAD 1.0 usa 6)
    try:
        from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog)
        from PySide6.QtCore import Qt
        using6 = True
    except Exception:
        from PySide2.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog)
        from PySide2.QtCore import Qt
        using6 = False

    class W(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Markov Tracer (Qt GUI)")
            self.resize(820, 480)
            self.script = QLineEdit(); self.args = QLineEdit()
            self.include = QLineEdit(); self.exclude = QLineEdit()
            self.log = QTextEdit(); self.log.setReadOnly(True)
            self.outdir = None

            top = QHBoxLayout()
            top.addWidget(QLabel("Script:")); top.addWidget(self.script, 1)
            b = QPushButton("Examinar…"); b.clicked.connect(self.pick); top.addWidget(b)

            row2 = QHBoxLayout(); row2.addWidget(QLabel("Args:")); row2.addWidget(self.args,1)
            row3 = QHBoxLayout(); row3.addWidget(QLabel("Include:")); row3.addWidget(self.include,1)
            row4 = QHBoxLayout(); row4.addWidget(QLabel("Exclude:")); row4.addWidget(self.exclude,1)

            row5 = QHBoxLayout()
            self.btn_run = QPushButton("Trazar"); self.btn_run.clicked.connect(self.run)
            self.btn_open = QPushButton("Abrir carpeta"); self.btn_open.clicked.connect(self.open_dir); self.btn_open.setEnabled(False)
            row5.addWidget(self.btn_run); row5.addWidget(self.btn_open)

            lay = QVBoxLayout(self)
            lay.addLayout(top); lay.addLayout(row2); lay.addLayout(row3); lay.addLayout(row4); lay.addLayout(row5)
            lay.addWidget(QLabel("Log:")); lay.addWidget(self.log,1)

        def pick(self):
            p, _ = QFileDialog.getOpenFileName(self, "Script Python", "", "Python (*.py)")
            if p: self.script.setText(p)

        def open_dir(self):
            if self.outdir and os.path.isdir(self.outdir):
                if sys.platform.startswith("win"): os.startfile(self.outdir)
                elif sys.platform == "darwin": subprocess.run(["open", self.outdir])
                else: subprocess.run(["xdg-open", self.outdir])

        def run(self):
            s = self.script.text().strip()
            if not s or not os.path.isfile(s):
                self._log("[ERROR] Selecciona un script .py válido."); return
            self.outdir = os.path.dirname(os.path.abspath(s))
            inc = [t.strip() for t in self.include.text().split(",") if t.strip()]
            exc = [t.strip() for t in self.exclude.text().split(",") if t.strip()]
            args = self.args.text().split()
            self._log(f"[INFO] Ejecutando {os.path.basename(s)} {' '.join(args)}")
            try:
                dot, png = trace_and_export(s, args, outdir=self.outdir,
                                            includes=inc, excludes=exc,
                                            mincount=1, want_png=True)
                self._log(f"[OK] DOT: {dot}")
                if png: self._log(f"[OK] PNG: {png}")
                else:   self._log("[INFO] Graphviz no disponible; sólo DOT.")
                self.btn_open.setEnabled(True)
            except Exception as ex:
                self._log(f"[ERROR] {ex}")

        def _log(self, m): self.log.append(m)

    app = QApplication.instance() or QApplication(sys.argv)
    w = W(); w.show()
    if not QApplication.instance():
        sys.exit(app.exec_() if not 'using6' in globals() or not using6 else app.exec())

# ----------------- CLI -----------------
def main_cli(argv):
    p = argparse.ArgumentParser(description="Grafo Markov-like de llamadas entre funciones al ejecutar un script Python.")
    p.add_argument("script", nargs="?", help="Ruta al script .py")
    p.add_argument("script_args", nargs=argparse.REMAINDER, help="Argumentos del script (después del .py)")
    p.add_argument("--png", action="store_true", help="Generar PNG (Graphviz)")
    p.add_argument("--outdir", default=None, help="Carpeta de salida (default: del script)")
    p.add_argument("--include", action="append", default=[], help="Incluir módulos que contengan este texto (repetible)")
    p.add_argument("--exclude", action="append", default=[], help="Excluir módulos que contengan este texto (repetible)")
    p.add_argument("--mincount", type=int, default=1, help="No dibujar aristas con conteo < N")
    p.add_argument("--gui", choices=["auto","tk","qt","none"], default="none", help="Lanzar GUI (auto/tk/qt/none)")
    args = p.parse_args(argv)

    # GUI?
    if args.gui != "none":
        if args.gui == "auto":
            if running_in_freecad():
                launch_qt_gui(); return 0
            # fuera de FreeCAD: intentar Tk
            try:
                import tkinter  # noqa
                launch_tk_gui(); return 0
            except Exception:
                # si Tk falla, intentar Qt (si PySide está instalado)
                try:
                    import PySide6  # noqa
                    launch_qt_gui(); return 0
                except Exception:
                    print("[INFO] No hay GUI disponible; usando CLI.")
        elif args.gui == "tk":
            launch_tk_gui(); return 0
        elif args.gui == "qt":
            launch_qt_gui(); return 0

    # CLI pura:
    if not args.script:
        p.print_help(); return 2
    dot, png = trace_and_export(args.script, args.script_args, outdir=args.outdir,
                                includes=args.include, excludes=args.exclude,
                                mincount=args.mincount, want_png=args.png)
    print(f"[OK] DOT: {dot}")
    print(f"[OK] PNG: {png}" if png else "[INFO] PNG no generado (usa --png y ten Graphviz).")
    return 0

if __name__ == "__main__":
    sys.exit(main_cli(sys.argv[1:]))
