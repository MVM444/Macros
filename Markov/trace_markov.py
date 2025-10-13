# trace_markov.py — genera un grafo estilo Markov de llamadas entre funciones
import sys, runpy, inspect, atexit, os
from collections import defaultdict

trans = defaultdict(int)
last = [None]  # stack-like storage of last function

def qualname(frame):
    mod = frame.f_globals.get("__name__", "?")
    func = frame.f_code.co_name
    if func == "<module>":
        return f"{mod}.__module__"
    cls = None
    if "self" in frame.f_locals:
        cls = type(frame.f_locals["self"]).__name__
    return f"{mod}.{cls+'.' if cls else ''}{func}"

def tracer(frame, event, arg):
    if event == "call":
        cur = qualname(frame)
        prev = last[0]
        if prev is not None:
            trans[(prev, cur)] += 1
        last[0] = cur
    elif event in ("return", "exception"):
        # on return, set last to caller if possible
        caller = frame.f_back
        last[0] = qualname(caller) if caller else None
    return tracer

def write_dot(out_path="markov.dot"):
    # sumariza probabilidades por origen
    by_src = defaultdict(int)
    for (src, dst), c in trans.items():
        by_src[src] += c
    lines = [
        'digraph G {',
        '  rankdir=LR;',
        '  node [shape=box, fontname="Arial"];'
    ]
    for (src, dst), c in trans.items():
        p = c / max(1, by_src[src])
        lines.append(f'  "{src}" -> "{dst}" [label="{c} | {p:.2f}"];')
    lines.append("}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] DOT escrito en {out_path}")
    if os.system("dot -V >nul 2>&1") == 0:
        os.system(f'dot -Tpng "{out_path}" -o "markov.png"')
        print("[OK] PNG generado: markov.png (requiere Graphviz)")

def main():
    if len(sys.argv) < 2:
        print("Uso: python trace_markov.py <script.py> [args...]")
        sys.exit(1)
    target = sys.argv[1]
    sys.settrace(tracer)
    atexit.register(write_dot)
    sys.argv = sys.argv[1:]  # pasa args al script objetivo
    runpy.run_path(target, run_name="__main__")

if __name__ == "__main__":
    main()
