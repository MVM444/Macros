from pathlib import Path
from pypdf import PdfReader
import re
paths = [Path(line.split('|')[0].strip()) for line in Path('limon_sucursal_mantenimiento.txt').read_text(encoding='utf-8').splitlines()]
for path in paths:
    try:
        reader = PdfReader(path)
    except Exception as exc:
        print('error', path, exc)
        continue
    text = "\n".join(page.extract_text() or "" for page in reader.pages[:5])
    text_low = text.lower()
    suc_idx = text_low.find('sucursal')
    lim_idx = text_low.find('limon')
    if suc_idx != -1 and lim_idx != -1:
        start = min(suc_idx, lim_idx)
        snippet = text[start:start+200]
        snippet_clean = ' '.join(snippet.replace('\n',' ').split())
        print('->', path)
        print(' snippet:', snippet_clean)
