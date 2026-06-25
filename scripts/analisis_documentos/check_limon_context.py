from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/04-Abril-2025/Upala/RODRIGUEZ/Anexo #12-Formulario F.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages)
lower = text.lower()
pos = 0
while True:
    idx = lower.find('limon', pos)
    if idx == -1:
        break
    start = max(0, idx-200)
    segment = text[start:idx+100]
    print('---', segment.replace('\n',' '))
    if 'sucursal' in segment.lower():
        print('  contains sucursal in same segment')
    pos = idx + 1
