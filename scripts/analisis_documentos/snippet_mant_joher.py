from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/04-Abril-2025/Upala/JOHER/3- EXPERIENCIA DE LA EMPRESA/1- EXPERIENCIA GENERAL JOHER S.A..pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages)
lower = text.lower()
idx = lower.find('mantenimiento')
if idx != -1:
    snippet = text[max(0, idx-120):idx+200]
    print(snippet.replace('\n',' ').strip())
