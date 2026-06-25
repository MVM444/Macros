from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/04-Abril-2025/Upala/RODRIGUEZ/Anexo #12-Formulario F.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages[:10])
if 'mantenimiento' in text.lower():
    print('mantenimiento found')
else:
    print('no mantenimiento')
print(text.lower().count('limon'))
