"""Convert vector PDF page geometry to an ASCII DXF (R12).

Designed for architectural sheets exported from CAD. PDF coordinates are
converted from points to millimetres and multiplied by the declared plot scale.
Cubic Bezier segments are tessellated because DXF R12 has no native Bezier.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pdfplumber


def bezier(p0, p1, p2, p3, steps=4):
    for i in range(1, steps + 1):
        t = i / steps
        u = 1.0 - t
        yield (
            u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
        )


def pair(code, value):
    return f"{code}\n{value}\n"


def add_line(out, a, b, layer="GEOMETRY", color=7):
    if math.dist(a, b) < 1e-9:
        return
    out.extend(
        [
            pair(0, "LINE"),
            pair(8, layer),
            pair(62, color),
            pair(10, f"{a[0]:.5f}"),
            pair(20, f"{a[1]:.5f}"),
            pair(30, "0"),
            pair(11, f"{b[0]:.5f}"),
            pair(21, f"{b[1]:.5f}"),
            pair(31, "0"),
        ]
    )


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: pdf_vector_to_dxf.py input.pdf output.dxf plot_scale")
    source, target, plot_scale = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
    factor = 25.4 / 72.0 * plot_scale
    out = [
        pair(0, "SECTION"),
        pair(2, "HEADER"),
        pair(9, "$ACADVER"),
        pair(1, "AC1009"),
        pair(9, "$INSUNITS"),
        pair(70, "4"),
        pair(0, "ENDSEC"),
        pair(0, "SECTION"),
        pair(2, "ENTITIES"),
    ]
    entity_count = 0

    with pdfplumber.open(source) as pdf:
        page = pdf.pages[0]

        def cv(p):
            return p[0] * factor, (page.height - p[1]) * factor

        for obj in [*page.curves]:
            current = None
            start = None
            color = 5 if obj.get("stroking_color") in ((0, 0, 1), [0, 0, 1]) else 7
            for command in obj.get("path", []):
                op, *values = command
                if op == "m":
                    current = values[0]
                    start = current
                elif op == "l" and current is not None:
                    endpoint = values[0]
                    add_line(out, cv(current), cv(endpoint), color=color)
                    entity_count += 1
                    current = endpoint
                elif op == "c" and current is not None:
                    p1, p2, endpoint = values
                    last = current
                    for point in bezier(current, p1, p2, endpoint):
                        add_line(out, cv(last), cv(point), color=color)
                        entity_count += 1
                        last = point
                    current = endpoint
                elif op == "h" and current is not None and start is not None:
                    add_line(out, cv(current), cv(start), color=color)
                    entity_count += 1
                    current = start

        for line in page.lines:
            add_line(out, cv((line["x0"], page.height - line["y0"])),
                     cv((line["x1"], page.height - line["y1"])))
            entity_count += 1

        for rect in page.rects:
            x0, x1 = rect["x0"], rect["x1"]
            top, bottom = rect["top"], rect["bottom"]
            pts = [(x0, top), (x1, top), (x1, bottom), (x0, bottom), (x0, top)]
            for a, b in zip(pts, pts[1:]):
                add_line(out, cv(a), cv(b), layer="RECTANGLES")
                entity_count += 1

        for word in page.extract_words(keep_blank_chars=False):
            x, y = cv((word["x0"], word["bottom"]))
            height = max(1.0, (word["bottom"] - word["top"]) * factor)
            out.extend(
                [
                    pair(0, "TEXT"),
                    pair(8, "TEXT"),
                    pair(10, f"{x:.5f}"),
                    pair(20, f"{y:.5f}"),
                    pair(30, "0"),
                    pair(40, f"{height:.5f}"),
                    pair(1, word["text"].replace("\n", " ")),
                ]
            )
            entity_count += 1

    out.extend([pair(0, "ENDSEC"), pair(0, "EOF")])
    target.write_text("".join(out), encoding="ascii", errors="replace")
    print(f"Created {target} with {entity_count} entities; scale factor {factor:.9f}")


if __name__ == "__main__":
    main()
