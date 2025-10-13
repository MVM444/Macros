# markov_tracer_gui.py
# GUI independiente (Tkinter) para trazar transiciones de llamadas entre funciones

import os
import runpy
import shlex
import shutil
import subprocess
import sys
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog, messagebox, ttk

# ----------- Nucleo de trazado -----------

_trans = defaultdict(int)
_last = [None]


def qualname(frame):
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
    return f"{mod}.{cls + '.' if cls else ''}{func}"


def tracer(frame, event, arg):
    if event == "call":
        cur = qualname(frame)
        prev = _last[0]
        if prev is not None:
            _trans[(prev, cur)] += 1
        _last[0] = cur
    elif event in ("return", "exception"):
        caller = frame.f_back
        _last[0] = qualname(caller) if caller else None
    return tracer


def write_dot(out_path="markov.dot"):
    by_src = defaultdict(int)
    for (src, dst), count in _trans.items():
        by_src[src] += count
    lines = [
        "digraph G {",
        "  rankdir=LR;",
        '  node [shape=box, fontname="Arial"];',
    ]
    for (src, dst), count in _trans.items():
        total = max(1, by_src[src])
        prob = count / total
        lines.append(f'  "{src}" -> "{dst}" [label="{count} | {prob:.2f}"];')
    lines.append("}")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return out_path


_DOT_PATH_HINTS = [
    os.environ.get("GRAPHVIZ_DOT"),
    "dot",
    r"C:\Program Files\Graphviz\bin\dot.exe",
    r"C:\Program Files (x86)\Graphviz\bin\dot.exe",
]


def get_dot_command():
    for candidate in _DOT_PATH_HINTS:
        if not candidate:
            continue
        if os.path.isabs(candidate):
            if os.path.isfile(candidate):
                return candidate
        else:
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
    return None


def has_graphviz():
    return get_dot_command() is not None


def dot_to_png(dot_path, png_path, dot_cmd=None):
    cmd = dot_cmd or get_dot_command()
    if not cmd:
        return False, "Graphviz (dot) no esta disponible."
    try:
        completed = subprocess.run(
            [cmd, "-Tpng", dot_path, "-o", png_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True, None
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode(errors="ignore") if exc.stderr else ""
        stderr = stderr.strip() or str(exc)
        return False, f"Error al ejecutar {cmd!r}: {stderr}"
    except Exception as exc:
        return False, f"No se pudo ejecutar {cmd!r}: {exc}"


# ----------- GUI -----------


class MarkovGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markov Tracer GUI (independiente)")
        self.geometry("760x480")

        self.script_path = tk.StringVar()
        self.args = tk.StringVar()
        self.new_arg = tk.StringVar()
        self.arg_items = []

        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Script:").grid(row=0, column=0, sticky="w")
        script_entry = ttk.Entry(frm, textvariable=self.script_path, width=60)
        script_entry.grid(row=0, column=1, sticky="we")
        ttk.Button(frm, text="Examinar...", command=self.browse).grid(row=0, column=2, padx=5)

        ttk.Label(frm, text="Argumentos manuales:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        manual_entry = ttk.Entry(frm, textvariable=self.args, width=60)
        manual_entry.grid(row=1, column=1, columnspan=2, sticky="we", pady=(10, 0))

        arg_frame = ttk.LabelFrame(frm, text="Argumentos predefinidos")
        arg_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        arg_frame.columnconfigure(0, weight=1)

        add_frame = ttk.Frame(arg_frame)
        add_frame.grid(row=0, column=0, sticky="ew", pady=(5, 0))
        add_frame.columnconfigure(1, weight=1)

        ttk.Label(add_frame, text="Nuevo argumento:").grid(row=0, column=0, sticky="w")
        new_arg_entry = ttk.Entry(add_frame, textvariable=self.new_arg)
        new_arg_entry.grid(row=0, column=1, sticky="ew", padx=5)
        new_arg_entry.bind("<Return>", lambda event: self.add_argument())
        ttk.Button(add_frame, text="Agregar", command=self.add_argument).grid(row=0, column=2, padx=5)
        ttk.Button(add_frame, text="Limpiar seleccion", command=self.clear_argument_checks).grid(row=0, column=3)

        self.check_container = ttk.Frame(arg_frame)
        self.check_container.grid(row=1, column=0, sticky="nsew", pady=(5, 5))
        self.check_container.columnconfigure(0, weight=1)
        arg_frame.rowconfigure(1, weight=1)

        ttk.Button(frm, text="Ejecutar trazado", command=self.run_trace).grid(row=3, column=0, pady=10, sticky="w")
        ttk.Button(frm, text="Abrir carpeta", command=self.open_dir).grid(row=3, column=1, pady=10, sticky="w")

        self.log = tk.Text(frm, wrap="word", height=12)
        self.log.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)

        frm.rowconfigure(2, weight=1)
        frm.rowconfigure(4, weight=1)
        frm.columnconfigure(1, weight=1)

        script_entry.focus_set()

    def browse(self):
        path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if path:
            self.script_path.set(path)

    def append_log(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def add_argument(self):
        value = self.new_arg.get().strip()
        if not value:
            return
        if any(item["text"] == value for item in self.arg_items):
            messagebox.showinfo("Aviso", "Ese argumento ya esta en la lista.")
            self.new_arg.set("")
            return
        var = tk.BooleanVar(value=True)
        row = len(self.arg_items)
        check = ttk.Checkbutton(self.check_container, text=value, variable=var)
        check.grid(row=row, column=0, sticky="w", pady=2)
        self.arg_items.append({"text": value, "var": var, "widget": check})
        self.new_arg.set("")

    def clear_argument_checks(self):
        for item in self.arg_items:
            item["var"].set(False)

    def _parse_manual_args(self):
        raw = self.args.get().strip()
        if not raw:
            return []
        try:
            return shlex.split(raw)
        except ValueError as exc:
            messagebox.showerror("Error", f"Argumentos invalidos: {exc}")
            return None

    def _selected_arguments(self):
        return [item["text"] for item in self.arg_items if item["var"].get()]

    def run_trace(self):
        script = self.script_path.get()
        if not os.path.isfile(script):
            messagebox.showerror("Error", "Selecciona un script valido.")
            return

        manual_args = self._parse_manual_args()
        if manual_args is None:
            return
        selected_args = self._selected_arguments()
        effective_args = manual_args + selected_args

        _trans.clear()
        _last[0] = None
        self.outdir = os.path.dirname(os.path.abspath(script))
        dot_path = os.path.join(self.outdir, "markov.dot")
        png_path = os.path.join(self.outdir, "markov.png")

        argv_saved = sys.argv[:]
        sys.argv = [script] + effective_args

        if effective_args:
            args_display = shlex.join(effective_args)
            self.append_log(f"[INFO] Ejecutando {os.path.basename(script)} {args_display}")
        else:
            self.append_log(f"[INFO] Ejecutando {os.path.basename(script)} (sin argumentos)")

        try:
            sys.settrace(tracer)
            runpy.run_path(script, run_name="__main__")
        except SystemExit:
            pass
        except Exception as exc:
            self.append_log(f"[ERROR] {exc}")
        finally:
            sys.settrace(None)
            sys.argv = argv_saved

        write_dot(dot_path)
        self.append_log(f"[OK] DOT generado en {dot_path}")

        success, message = dot_to_png(dot_path, png_path)
        if success:
            self.append_log(f"[OK] PNG generado en {png_path}")
        else:
            warn_msg = message or "No se pudo generar el PNG."
            self.append_log(f"[WARN] {warn_msg}")

    def open_dir(self):
        if self.outdir and os.path.isdir(self.outdir):
            if sys.platform.startswith("win"):
                os.startfile(self.outdir)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.outdir], check=False)
            else:
                subprocess.run(["xdg-open", self.outdir], check=False)
        else:
            messagebox.showinfo("Aviso", "Genera un trazado antes de abrir la carpeta.")


if __name__ == "__main__":
    app = MarkovGUI()
    app.mainloop()
