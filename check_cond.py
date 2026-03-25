from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/Mantenimiento/Condiciones especiïficas para la contratacioïn de Servicios de Mantenimiento preventivo y correctivo con suministro de repuestos.pdf")
reader = PdfReader(path)
text = "\n".join((page.extract_text() or "") for page in reader.pages[:15])
print('limon' in text.lower())
