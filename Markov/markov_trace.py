#!/usr/bin/env python
# markov_trace.py
# Traza llamadas entre funciones mientras ejecuta un script objetivo y genera:
#  - markov.dot (siempre)
#  - markov.png (si tienes Graphviz "dot" en el PATH o usas --png)
#
# Uso:
#   python markov_trace.py TU_SCRIPT.py [args del script...] --png
#
# Filtros útiles:
#   --include paquete_o_modulo   (se puede repetir)
#   --exclude paquete_o_modulo   (se puede repetir)
#   --mincount N                 (no dibuja aristas con conteo < N)
#
# Ejemplos:
#   python markov_trace.py ejemplo.py --png
#   python markov_trace.py ejemplo.py --include mi_paquete --mincount 2 --png
#   python markov_trace.py ejemplo.py arg1 arg2 --exclude site-packages --png

import sys, os, runpy, atexit, argparse, subprocess
from collections import defaultdict

# ---------- utilidades ----------
def has_graphviz():
    try:
        subprocess.run(["dot", "-V"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except Exception:
        return False

def dot_to_png(dot_path, png_path):
    try:
        subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path], check=True)
        return True
    except Exception:
        return False

def norm_path(p):
    try:
        return os.path.normpath(os.path.abspath(p))
    except Exception:
        return p

# ---------- formateo de nombres ----------
def qualname(frame):
    """Construye nombre calificado: modulo(.Clase).funcion  /  modulo.__module__ para nivel toplevel"""
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

# ---------- trazado ----------
class CallTracer:
    def __init__(self, includes, excludes, mincount):
        # includes/excludes son listas de substrings a buscar en el "modulo" del qualname
        self.includes = includes or []
        self.excludes = excludes or []
        self.mincount = max(1, int(mincount))
        self.trans = defaultdict(int)   # ((src,dst) -> conteo)
        self.by_src = defaultdict(int)  # src -> total
        self._last = None

    def _allowed_mod(self, qname):
        # decide si un qname pasa filtros
        # qname = "modulo.Cls.func" ; modulo es la primera parte antes del primer '.'
        mod = qname.split(".", 1)[0]
        if self.includes:
            if not any(tok in mod for tok in self.includes):
                return False
        if self.excludes:
            if any(tok in mod for tok in self.excludes):
                return False
        return True

    def tracer(self, frame, event, arg):
        try:
            if event == "call":
                cur = qualname(frame)
                if not self._allowed_mod(cur):
                    # no actualizamos _last si el actual no pasa el filtro,
                    # pero sí dejamos que _last se mantenga
                    return self.tracer
                prev = self._last
                if prev is not None and self._allowed_mod(prev):
                    self.trans[(prev, cur)] += 1
                self._last = cur
            elif event in ("return", "exception"):
                # al retornar, retrocedemos a quien llamó (si califica)
                caller = frame.f_back
                self._last = qualname(caller) if caller else None
        except Exception:
            # nunca abortar el trazador por una excepción aquí
            pass
        return self.tracer

    def finalize(self):
        # sumariza por origen
        self.by_src.clear()
        for (src, dst), c in self.trans.items():
            if c >= self.mincount:
                self.by_src[src] += c

    def write_dot(self, out_path):
        lines = [
            "digraph G {",
            "  rankdir=LR;",
            '  node [shape=box, fontname="Arial"];'
        ]
        for (src, dst), c in self.trans.items():
            if c < self.mincount:
                continue
            total = max(1, self.by_src[src])
            p = c / total
            # escapado básico de comillas
            s = src.replace('"', r'\"')
            d = dst.replace('"', r'\"')
            lines.append(f'  "{s}" -> "{d}" [label="{c} | {p:.2f}"];')
        lines.append("}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return out_path

# ---------- main ----------
def main():
    parser = argparse.ArgumentParser(description="Trazar grafo estilo Markov de llamadas entre funciones al ejecutar un script Python.")
    parser.add_argument("script", help="Ruta al script .py objetivo")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Argumentos para el script")
    parser.add_argument("--png", action="store_true", help="Intentar generar markov.png usando Graphviz")
    parser.add_argument("--outdir", default=None, help="Carpeta de salida (por defecto, la del script)")
    parser.add_argument("--include", action="append", default=[], help="Filtrar: incluir módulos que CONTENGAN este texto (repetible)")
    parser.add_argument("--exclude", action="append", default=[], help="Filtrar: excluir módulos que CONTENGAN este texto (repetible)")
    parser.add_argument("--mincount", type=int, default=1, help="No dibuja aristas con conteo menor a este valor (default=1)")

    args = parser.parse_args()

    script_path = norm_path(args.script)
    if not os.path.isfile(script_path):
        print(f"[ERROR] Script no encontrado: {script_path}")
        sys.exit(2)

    outdir = norm_path(args.outdir) if args.outdir else os.path.dirname(script_path)
    os.makedirs(outdir, exist_ok=True)
    dot_path = os.path.join(outdir, "markov.dot")
    png_path = os.path.join(outdir, "markov.png")

    tracer = CallTracer(includes=args.include, excludes=args.exclude, mincount=args.mincount)

    # preparar argv para el script objetivo
    saved_argv = sys.argv[:]
    sys.argv = [script_path] + args.script_args

    # ejecutar bajo sys.settrace
    try:
        sys.settrace(tracer.tracer)
        try:
            runpy.run_path(script_path, run_name="__main__")
        finally:
            sys.settrace(None)
    except SystemExit:
        # permitir sys.exit() en el script objetivo
        pass
    finally:
        sys.argv = saved_argv

    tracer.finalize()
    tracer.write_dot(dot_path)
    print(f"[OK] DOT: {dot_path}")

    if args.png:
        if has_graphviz():
            if dot_to_png(dot_path, png_path):
                print(f"[OK] PNG: {png_path}")
            else:
                print("[WARN] No se pudo generar PNG con dot.")
        else:
            print("[WARN] Graphviz no detectado en PATH; omitiendo PNG (usa --png con Graphviz instalado).")

if __name__ == "__main__":
    main()
