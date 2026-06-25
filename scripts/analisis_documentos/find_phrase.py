from pathlib import Path
from pypdf import PdfReader
import unicodedata
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
phrase = 'sucursal de limon'
matches = []
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
    except Exception:
        continue
    text = "\n".join((page.extract_text() or "") for page in reader.pages[:10])
    norm = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    if phrase in norm and 'mantenimiento' in text.lower():
        snippet = text.lower()
        matches.append((path, snippet[:400]))
        if len(matches) >= 3:
            break
with open('sucursal_limon_phrase.txt', 'w', encoding='utf-8') as fh:
    for path, snippet in matches:
        fh.write(str(path) + '\n' + snippet + '\n---\n')
print('found', len(matches))
