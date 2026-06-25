from pathlib import Path
from docx import Document
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
keywords = ['sucursal', 'limon', 'mantenimiento']
results = []
for path in sorted(root.rglob("*.docx")):
    try:
        doc = Document(path)
    except Exception:
        continue
    text = "\n".join(p.text for p in doc.paragraphs)
    lower = text.lower()
    if all(k in lower for k in keywords):
        snippet = lower
        results.append((path, snippet[:400]))
        if len(results) >= 5:
            break
with open('docx_matches.txt', 'w', encoding='utf-8') as fh:
    for path, snippet in results:
        fh.write(str(path) + '\n' + snippet + '\n\n')
print('found', len(results))
