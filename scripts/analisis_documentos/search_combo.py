from pathlib import Path
from pypdf import PdfReader
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025")
keywords = ["sucursal", "limon", "mantenimiento"]
matches = []
for path in sorted(root.rglob("*.pdf")):
    try:
        reader = PdfReader(path)
    except Exception:
        continue
    text_accum = ""
    found = False
    for page in reader.pages[:8]:
        text = page.extract_text() or ""
        text_accum += text + "\n"
        lower = text_accum.lower()
        if all(k in lower for k in keywords):
            idx = lower.index("limon")
            snippet = text_accum[max(0, idx-200):idx+200].replace('\n',' ')
            matches.append((path, snippet.strip()))
            found = True
            break
    if found and len(matches) >= 5:
        break
with open('sucursal_limon_maint.txt', 'w', encoding='utf-8') as fh:
    for path, snippet in matches:
        fh.write(f"{path}\n{snippet}\n\n")
print('matches', len(matches))
