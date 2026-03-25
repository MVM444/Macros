from pathlib import Path
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/Mantenimiento")
keywords = ["limon", "mantenimiento"]
matches = []
for path in sorted(root.glob("*.pdf")):
    try:
        reader = PdfReader(path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages[:5])
    except Exception as exc:
        continue
    txt = text.lower()
    if keywords[0] in txt and keywords[1] in txt:
        matches.append(path)
with open('limon_maint_matches.txt', 'w', encoding='utf-8') as fh:
    for m in matches:
        fh.write(str(m) + '\n')
print('matches', len(matches))
