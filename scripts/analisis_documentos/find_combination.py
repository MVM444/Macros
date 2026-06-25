from pathlib import Path
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
keywords = ["sucursal", "limon", "mantenimiento"]
results = []
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
    except Exception:
        continue
    text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
    lower = text.lower()
    if all(k in lower for k in keywords):
        results.append((path, lower.count('limon')))
with open('limon_sucursal_mantenimiento.txt', 'w', encoding='utf-8') as fh:
    for path, count in results:
        fh.write(f"{path} | limon_count={count}\n")
print('found', len(results))
