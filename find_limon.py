from pathlib import Path
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
keyword = "limon"
result = []
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
    except Exception:
        continue
    if keyword in text.lower():
        result.append(path)
with open('limon_found.txt', 'w', encoding='utf-8') as fh:
    for p in result:
        fh.write(str(p) + '\n')
print('found', len(result), 'files')
