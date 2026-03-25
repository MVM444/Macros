from pathlib import Path
from pypdf import PdfReader
import unicodedata
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
phrase = 'sucursal de limon'
match = None
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
    except Exception:
        continue
    page_text = []
    for i, page in enumerate(reader.pages):
        if i >= 20:
            break
        text = page.extract_text() or ""
        page_text.append(text)
        norm = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
        if phrase in norm and 'mantenimiento' in text.lower():
            snippet = text.replace('\n', ' ')
            match = (path, snippet[:400])
            break
    if match:
        break
if match:
    with open('sucursal_de_limon_doc.txt', 'w', encoding='utf-8') as fh:
        fh.write(str(match[0]) + '\n' + match[1])
    print('found', match[0])
else:
    print('not found')
