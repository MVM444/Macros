from __future__ import annotations

import difflib
import json
import re
import unicodedata
from pathlib import Path


BASE = Path(__file__).resolve().parent / "index"
DOCX_INPUT = BASE / "docx_sources.json"
PDF_INPUT = BASE / "sources.json"
OUTPUT = BASE / "history_analysis.json"


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip().casefold()


def meaningful_paragraphs(doc: dict[str, object]) -> list[dict[str, object]]:
    ignored = {
        "atentamente,",
        "equipo de infraestructura y mantenimiento de la gerencia financiera",
        "marco vinicio mora fallas",
        "ing. electromecánico",
    }
    result = []
    for paragraph in doc["paragraphs"]:
        norm = normalized(paragraph["text"])
        if not norm or norm in ignored:
            continue
        if re.fullmatch(r"gf-eim-it-\d{4}-20\d{2}", norm):
            continue
        result.append(paragraph)
    return result


def diff_docs(
    old_doc: dict[str, object], new_doc: dict[str, object]
) -> dict[str, object]:
    old_paragraphs = meaningful_paragraphs(old_doc)
    new_paragraphs = meaningful_paragraphs(new_doc)
    old_norm = [normalized(item["text"]) for item in old_paragraphs]
    new_norm = [normalized(item["text"]) for item in new_paragraphs]
    matcher = difflib.SequenceMatcher(a=old_norm, b=new_norm, autojunk=False)

    changes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        changes.append(
            {
                "operation": tag,
                "old": [
                    {
                        "index": item["index"],
                        "style": item["style"],
                        "text": item["text"],
                    }
                    for item in old_paragraphs[i1:i2]
                ],
                "new": [
                    {
                        "index": item["index"],
                        "style": item["style"],
                        "text": item["text"],
                    }
                    for item in new_paragraphs[j1:j2]
                ],
            }
        )

    return {
        "old": old_doc["filename"],
        "new": new_doc["filename"],
        "sequence_similarity": matcher.ratio(),
        "old_paragraphs": len(old_paragraphs),
        "new_paragraphs": len(new_paragraphs),
        "change_blocks": changes,
    }


def main() -> None:
    docs = json.loads(DOCX_INPUT.read_text(encoding="utf-8"))
    pdfs = json.loads(PDF_INPUT.read_text(encoding="utf-8"))
    docs_by_name = {item["filename"]: item for item in docs}

    version_order = [
        "GF-EIM-IT-0001-2023---Esp. Tec. AA Norte.docx",
        "GF-EIM-IT-0053-2024---Esp. Tec. Aires Acondicionados.docx",
        "GF-EIM-IT-0019-2025---Esp. Tec. Aires Acondicionados.docx",
        "GF-EIM-IT-0031-2025---Esp. Tec. Aires Acondicionados.docx",
    ]
    deltas = [
        diff_docs(docs_by_name[old_name], docs_by_name[new_name])
        for old_name, new_name in zip(version_order, version_order[1:])
    ]

    hash_groups: dict[str, list[str]] = {}
    for pdf in pdfs:
        hash_groups.setdefault(pdf["sha256"], []).append(pdf["path"])
    exact_duplicates = [
        paths for paths in hash_groups.values() if len(paths) > 1
    ]

    text_groups: dict[str, list[str]] = {}
    for pdf in pdfs:
        text_key = normalized(pdf["text"])
        if text_key:
            text_groups.setdefault(text_key, []).append(pdf["path"])
    same_extracted_text = [
        paths for paths in text_groups.values() if len(paths) > 1
    ]

    result = {
        "version_order": version_order,
        "version_deltas": deltas,
        "exact_pdf_duplicate_groups": exact_duplicates,
        "same_extracted_text_groups": same_extracted_text,
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "version_deltas": [
                    {
                        "old": item["old"],
                        "new": item["new"],
                        "sequence_similarity": round(
                            item["sequence_similarity"], 4
                        ),
                        "change_blocks": len(item["change_blocks"]),
                    }
                    for item in deltas
                ],
                "exact_pdf_duplicate_groups": len(exact_duplicates),
                "same_extracted_text_groups": len(same_extracted_text),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
