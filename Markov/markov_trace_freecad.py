# markov_trace_freecad.py
# GUI Qt para ejecutar un script .py desde FreeCAD y generar un grafo de transiciones (DOT/PNG)
# - No usa Tk
# - No llama sys.exit()
# - Usa la QApplication existente de FreeCAD

import sys, os, runpy, subprocess
from collections import defaultdict

# ---------------- Núcleo de trazado ----------------

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

def _make_tracer(includes=None, excludes=None):
    includes = includes or []
    excludes = excludes or []
    def _allowed(qname):
        mod = qname.split(".", 1)[0]
        if includes and not any(tok in mod for tok in includes): return False
        if excludes and any(tok in mod for tok in excludes): return False
        return True
    def _tracer(frame, event, arg):
        try:
            if event == "call":
                cur = _qualname(frame)
                if not _allowed(cur):
                    return _tracer
                prev = _last[0]
                if prev is not None and _allowed(prev):
                    _trans[(prev, cur)] += 1
                _last[0] = cur
            elif event in ("return", "exception"):
                caller = frame.f_back
                _last[0] = _qualname(caller) if caller else None
        except Exception:
            pass
        return _tracer
    return _tracer

def _write_dot(out_path, mincount=1):
    # mincount: no dibujar aristas con conteo menor
    by_src = defaultdict(int)
    for (src, dst), c in _trans.items():
        if c >= mincount:
            by_src[src] += c
    lines = ["digraph G {", "  rankdir=LR;", '  node [shape=box, fontname="Arial"];']
    for (src, dst), c in _trans.items():
        if c < mincount: 
            continue
        total = max(1, by_src[src])
        p = c / total
        s = src.replace('"', r'\"')
        d = dst.replace('"', r'\"')
        lines.append(f'  "{s}" -> "{d}" [label="{c} | {p:.2f}"];')
    lines.append("}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path

def _has_graphviz():
    try:
        subprocess.run(["dot","-V"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except Exception:
        return False

def _dot_to_png(dot_path, png_path):
    try:
        subprocess.run(["dot","-Tpng", dot_path, "-o", png_path], check=True)
        return True
    except Exception:
        return False

def trace_and_export(target_script, script_args=None, outdir=None,
                     includes=None, excludes=None, mincount=1, want_png=True):
    """Ejecuta target_script bajo sys.settrace y genera markov.dot (+ .png opcional)."""
    _trans.clear()
    _last[0] = None
    target_script = os.path.abspath(target_script)
    outdir = outdir or os.path.dirname(target_script)
    os.makedirs(outdir, exist_ok=True)
    dot_path = os.path.join(outdir, "markov.dot")
    png_path = os.path.join(outdir, "markov.png")

    tracer = _make_tracer(includes, excludes)
    saved_argv = sys.argv[:]
    sys.argv = [target_script] + (script_args or [])

    try:
        sys.settrace(tracer)
        try:
            runpy.run_path(target_script, run_name="__main__")
        finally:
            sys.settrace(None)
    except SystemExit:
        # permitir scripts que llamen sys.exit() sin cerrar FreeCAD
        pass
    finally:
        sys.argv = saved_argv

    _write_dot(dot_path, mincount=mincount)
    png_ok = False
    if want_png and _has_graphviz():
        png_ok = _dot_to_png(dot_path, png_path)
    return dot_path, (png_path if png_ok else None)

# ---------------- GUI Qt (PySide) ----------------

# Intentar PySide6 (FreeCAD 1.0) y si no, PySide2 (FreeCAD 0.20/0.21)
try:
    from PySide6.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                                   QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QCheckBox)
    from PySide6.QtCore import Qt
    USING_PYSIDE6 = True
except Exception:
    from PySide2.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                                   QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QCheckBox)
    from PySide2.QtCore import Qt
    USING_PYSIDE6 = False

class MarkovFreeCAD(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Markov Tracer (FreeCAD Qt GUI)")
        self.resize(850, 520)

        # Widgets
        self.ed_script = QLineEdit()
        self.ed_args   = QLineEdit()
        self.ed_inc    = QLineEdit()
        self.ed_exc    = QLineEdit()
        self.chk_png   = QCheckBox("Generar PNG (Graphviz)")
        self.chk_png.setChecked(True)
        self.ed_minc   = QLineEdit("1")
        self.log       = QTextEdit(); self.log.setReadOnly(True)

        # Layout top: script + examinar
        row0 = QHBoxLayout()
        row0.addWidget(QLabel("Script .py:"))
        row0.addWidget(self.ed_script, 1)
        btn_browse = QPushButton("Examinar…")
        btn_browse.clicked.connect(self.pick_script)
        row0.addWidget(btn_browse)

        # Args / filtros
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Args:"))
        row1.addWidget(self.ed_args, 1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Include:"))
        row2.addWidget(self.ed_inc, 1)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Exclude:"))
        row3.addWidget(self.ed_exc, 1)

        row4 = QHBoxLayout()
        row4.addWidget(self.chk_png)
        row4.addWidget(QLabel("Min conteo:"))
        row4.addWidget(self.ed_minc)
        row4.addStretch(1)

        # Botones ejecutar / abrir carpeta
        row_btns = QHBoxLayout()
        btn_run  = QPushButton("Trazar")
        btn_open = QPushButton("Abrir carpeta")
        btn_run.clicked.connect(self.run_trace)
        btn_open.clicked.connect(self.open_outdir)
        row_btns.addWidget(btn_run)
        row_btns.addWidget(btn_open)
        row_btns.addStretch(1)

        # Layout principal
        lay = QVBoxLayout(self)
        lay.addLayout(row0)
        lay.addLayout(row1)
        lay.addLayout(row2)
        lay.addLayout(row3)
        lay.addLayout(row4)
        lay.addLayout(row_btns)
        lay.addWidget(QLabel("Log:"))
        lay.addWidget(self.log, 1)

        self.outdir = None

    def pick_script(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar script Python", "", "Python (*.py)")
        if path:
            self.ed_script.setText(path)

    def log_msg(self, text):
        self.log.append(text)

    def open_outdir(self):
        if self.outdir and os.path.isdir(self.outdir):
            if sys.platform.startswith("win"):
                os.startfile(self.outdir)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.outdir])
            else:
                subprocess.run(["xdg-open", self.outdir])

    def run_trace(self):
        script = self.ed_script.text().strip()
        if not script or not os.path.isfile(script):
            self.log_msg("[ERROR] Selecciona un script .py válido.")
            return
        self.outdir = os.path.dirname(os.path.abspath(script))
        args = [a for a in self.ed_args.text().split() if a.strip()]
        inc  = [t.strip() for t in self.ed_inc.text().split(",") if t.strip()]
        exc  = [t.strip() for t in self.ed_exc.text().split(",") if t.strip()]
        try:
            minc = max(1, int(self.ed_minc.text()))
        except Exception:
            minc = 1
            self.ed_minc.setText("1")

        self.log_msg(f"[INFO] Ejecutando {os.path.basename(script)} {' '.join(args)}")
        try:
            dot, png = trace_and_export(script, args, outdir=self.outdir,
                                        includes=inc, excludes=exc,
                                        mincount=minc, want_png=self.chk_png.isChecked())
            self.log_msg(f"[OK] DOT: {dot}")
            if png:
                self.log_msg(f"[OK] PNG: {png}")
            else:
                self.log_msg("[INFO] PNG no generado (no hay Graphviz o está desactivado).")
        except Exception as ex:
            self.log_msg(f"[ERROR] {ex}")

# ---------- Lanzador para usar desde FreeCAD ----------

def launch_qt_gui_freecad():
    """Muestra la ventana sin cerrar FreeCAD."""
    app = QApplication.instance()
    if app is None:
        # En FreeCAD normalmente ya existe; si no, crear uno sin sys.exit()
        app = QApplication(sys.argv)
    w = MarkovFreeCAD()
    w.show()
    # No llamar sys.exit(). Si se ejecuta fuera de un loop activo:
    if not QApplication.instance():
        # caso raro, pero por seguridad; normalmente FreeCAD ya tiene el loop corriendo
        app.exec_() if not USING_PYSIDE6 else app.exec()

# Sugerido: permitir import y un pequeño "main" seguro
if __name__ == "__main__":
    # Si por casualidad ejecutas este archivo con Python normal, abre la GUI Qt.
    launch_qt_gui_freecad()
