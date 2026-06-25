from pathlib import Path
from pypdf import PdfReader
path = Path(r"C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\EIMGF\2025\Informes TEC 2025 PDF\(948916) GF-EIM-IT-0001-2025  ESPECIFICACIONES TECNICAS PARA ARRENDAMIENTO DE LOCAL SUCURSAL DE NICOYA (2).pdf")
reader = PdfReader(path)
text = reader.pages[0].extract_text()
print(text[:1000])
