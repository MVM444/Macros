from pathlib import Path
from pypdf import PdfReader
paths = [Path(line.strip()) for line in Path('limon_mantenimiento_match.txt').read_text(encoding='utf-8').splitlines()]
for path in paths:
    try:
        reader = PdfReader(path)
    except Exception as e:
        print('error', path, e)
        continue
    text = "\n".join((page.extract_text() or "") for page in reader.pages[:5])
    text_lower = text.lower()
    idx = text_lower.find('limon')
    idx2 = text_lower.find('mantenimiento')
    snippet = text[max(0, idx-100):idx+200] if idx != -1 else ''
    snippet2 = text[max(0, idx2-100):idx2+200] if idx2 != -1 else ''
    print('----')
    print(path)
    if idx != -1:
        print('limon snippet:', snippet.replace('\n',' ').strip())
    if idx2 != -1:
        print('mantenimiento snippet:', snippet2.replace('\n',' ').strip())
