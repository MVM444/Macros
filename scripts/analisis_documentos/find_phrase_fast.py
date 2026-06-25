from pathlib import Path
from pypdf import PdfReader
import unicodedata
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
phrase = 'sucursal de lim'
found = None
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
    except Exception:
        continue
    for page in reader.pages[:10]:
        text = page.extract_text() or ""
        norm = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
        if phrase in norm and 'mantenimiento' in text.lower():
            snippet = text.replace('\n', ' ')
            found = (path, snippet[:500])
            break
    if found:
        break
if found:
    with open('sucursal_limon_phrase_fast.txt', 'w', encoding='utf-8') as fh:
        fh.write(str(found[0]) + '\n' + found[1])
    print('found', found[0])
else:
    print('not found')
