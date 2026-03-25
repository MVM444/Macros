from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/08-Agosto-2025/Aires Acondicionados/Ubicacion de las Unidades Solicitantes e Informacion de pago.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages)
lower = text.lower()
idx = 0
while True:
    found = lower.find('limon', idx)
    if found == -1:
        break
    snippet = text[max(0, found-120):found+200]
    print('---')
    print(snippet.replace('\n',' '))
    idx = found + 1
