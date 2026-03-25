from pathlib import Path
from pypdf import PdfReader
import json
root = Path(r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\EIMGF\2025")
entries = []
for path in sorted(root.rglob("*.pdf")):
    rel = path.relative_to(root)
    try:
        reader = PdfReader(path)
        text_parts = []
        for i, page in enumerate(reader.pages[:2]):
            text = page.extract_text()
            if text:
                text_parts.append(text)
        text_all = "\n".join(text_parts)
        if text_all:
            lines = [line.strip() for line in text_all.splitlines() if line.strip()]
            first_line = lines[0] if lines else "<sin texto>"
        else:
            lines = []
            first_line = "<sin texto>"
        snippet = text_all[:400].replace('\n', ' ') if text_all else "<sin texto>"
        subject = next((line for line in lines if line.upper().startswith("ASUNTO")), "")
        antecedent = next((line for line in lines if "ANTECED" in line.upper()), "")
        reference = next((line for line in lines if "OFICIO" in line.upper() or "REFERENCIA" in line.upper()), "")
    except Exception as exc:
        text_all = ""
        first_line = f"<error: {exc}>"
        snippet = ""
        subject = ""
        antecedent = ""
        reference = ""
    entries.append({
        "path": str(rel),
        "first_line": first_line,
        "snippet": snippet,
        "subject": subject,
        "antecedent": antecedent,
        "reference": reference,
    })
with open("pdf_summaries_v2.json", "w", encoding="utf-8") as fh:
    json.dump(entries, fh, ensure_ascii=False, indent=2)
print(f"Wrote {len(entries)} entries to pdf_summaries_v2.json")
