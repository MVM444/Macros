from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/04-Abril-2025/Upala/RODRIGUEZ/Anexo #12-Formulario F.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages[:15])
low = text.lower()
idx = low.find('sucursal')
if idx != -1:
    snippet = text[max(0, idx-150):idx+150]
    print('snippet', snippet.replace('\n',' '))
else:
    print('no sucursal string')
print('---')
idx2 = low.find('limon')
if idx2 != -1:
    snippet2 = text[max(0, idx2-150):idx2+150]
    print('limon snippet', snippet2.replace('\n',' '))
else:
    print('no limon string')
