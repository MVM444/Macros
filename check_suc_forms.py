from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/04-Abril-2025/Upala/RODRIGUEZ/Anexo #12-Formulario F.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages)
lower = text.lower()
print('sucursal occurrences', lower.count('sucursal'))
for idx in range(0, len(lower)):
    found = lower.find('sucursal', idx)
    if found == -1:
        break
    snippet = text[max(0, found-100):found+160]
    print('snippet:', snippet.replace('\n',' '))
    idx = found + 1
    if lower.count('sucursal', found+1) > 5:
        break
