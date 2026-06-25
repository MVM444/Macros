from pathlib import Path
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
keywords = ["limon", "mantenimiento"]
results = []
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
    except Exception as exc:
        continue
    lower = text.lower()
    if all(k in lower for k in keywords):
        results.append(path)
with open('limon_mantenimiento.txt', 'w', encoding='utf-8') as fh:
    for result in results:
        fh.write(str(result) + '\n')
print('found', len(results), 'files')
