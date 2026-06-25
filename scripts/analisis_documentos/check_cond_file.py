from pathlib import Path
import unicodedata
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/Mantenimiento")
target = None
for path in root.iterdir():
    if not path.name.lower().startswith('condiciones'):
        continue
    target = path
    break
if not target:
    raise SystemExit('not found')
reader = PdfReader(target)
text = "\n".join((page.extract_text() or "") for page in reader.pages[:20])
print('limon' in text.lower())
print(text.lower().count('limon'))
print('mantenimiento' in text.lower())
print(text.lower().count('mantenimiento'))
if 'limon' in text.lower():
    idx = text.lower().find('limon')
    snippet = text[max(0, idx-100):idx+200]
    print('snippet limon', snippet.replace('\n',' '))
if 'mantenimiento' in text.lower():
    idx = text.lower().find('mantenimiento')
    snippet = text[max(0, idx-100):idx+200]
    print('snippet mantenimiento', snippet.replace('\n',' '))
