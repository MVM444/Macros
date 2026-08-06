from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


SOURCE_ROOT = Path(
    r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\EIMGF"
)
OUTPUT_DIR = Path(__file__).resolve().parent / "index"


def plain(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return value.lower()


def has_topic(filename: str) -> bool:
    text = plain(filename)
    return bool(
        "gf-eim-n-0032-2026" in text
        or
        re.search(r"\baires?\W{0,8}acondicionad", text)
        or re.search(r"(?<![a-z])a[\W_]*a(?![a-z])", text)
    )


def classify(filename: str) -> str | None:
    text = plain(filename)
    if not has_topic(filename):
        return None
    if re.search(r"(esp[^a-z0-9]*tec|especificacion)", text):
        if "mante" in text:
            return "especificacion_mantenimiento"
        if re.search(r"instal", text):
            return "especificacion_instalacion"
        return "especificacion_compra_instalacion"
    if re.search(r"(nota\W*aclar|aclaracion|modificacion|ampliacion)", text):
        return "aclaracion_modificacion"
    if re.search(r"(mante|reparacion|emergencia)", text):
        return "mantenimiento_reparacion"
    if re.search(r"(instal|tuberia)", text):
        return "instalacion"
    if re.search(r"(respuesta|recepcion|inspeccion|visita)", text):
        return "respuesta_inspeccion_recepcion"
    return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_pdf(path: Path) -> tuple[int, list[str], str | None]:
    try:
        reader = PdfReader(str(path))
        pages = [(page.extract_text() or "") for page in reader.pages]
        return len(reader.pages), pages, None
    except Exception as exc:  # preserve unreadable candidates in the inventory
        return 0, [], f"{type(exc).__name__}: {exc}"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for path in SOURCE_ROOT.rglob("*.pdf"):
        category = classify(path.name)
        if category is None:
            continue

        relative = path.relative_to(SOURCE_ROOT)
        year_match = re.search(r"(20\d{2})", str(relative))
        year = int(year_match.group(1)) if year_match else None
        if year is None or year < 2009 or year > 2026:
            continue

        page_count, pages, error = extract_pdf(path)
        text = "\n\n".join(pages)
        page_lengths = [len(page.strip()) for page in pages]
        row = {
            "year": year,
            "category": category,
            "signed": bool(re.search(r"firmad", plain(path.name))),
            "filename": path.name,
            "path": str(path),
            "relative_path": str(relative),
            "size_bytes": path.stat().st_size,
            "modified": path.stat().st_mtime,
            "sha256": sha256(path),
            "pages": page_count,
            "text_chars": len(text),
            "page_text_chars": page_lengths,
            "pages_text": pages,
            "extract_error": error,
            "text": text,
        }
        rows.append(row)

    rows.sort(
        key=lambda row: (
            -int(row["year"]),
            -int(bool(row["signed"])),
            str(row["filename"]).lower(),
        )
    )

    with (OUTPUT_DIR / "sources.json").open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)

    csv_fields = [
        "year",
        "category",
        "signed",
        "filename",
        "path",
        "relative_path",
        "size_bytes",
        "modified",
        "sha256",
        "pages",
        "text_chars",
        "page_text_chars",
        "extract_error",
    ]
    with (OUTPUT_DIR / "sources.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in csv_fields})

    by_year: dict[int, int] = {}
    by_category: dict[str, int] = {}
    for row in rows:
        by_year[int(row["year"])] = by_year.get(int(row["year"]), 0) + 1
        category = str(row["category"])
        by_category[category] = by_category.get(category, 0) + 1

    summary = {
        "source_root": str(SOURCE_ROOT),
        "candidate_count": len(rows),
        "years": dict(sorted(by_year.items(), reverse=True)),
        "categories": dict(sorted(by_category.items())),
        "extract_errors": sum(bool(row["extract_error"]) for row in rows),
        "low_text_pdfs": sum(
            int(row["pages"]) > 0 and int(row["text_chars"]) < 100
            for row in rows
        ),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
