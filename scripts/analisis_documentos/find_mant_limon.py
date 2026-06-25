from pathlib import Path
from pypdf import PdfReader
paths = [Path(line.strip()) for line in Path('limon_found.txt').read_text(encoding='utf-8').splitlines() if line.strip()]
key = 'mantenimiento'
matches = []
for path in paths:
    try:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages[:5])
    except Exception:
        continue
    if key in text.lower():
        matches.append((path, text))
with open('limon_mantenimiento_match.txt', 'w', encoding='utf-8') as fh:
    for path, text in matches:
        fh.write(str(path) + '\n')
print('found', len(matches))
