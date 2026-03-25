import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import unicodedata
root = Path(r"C:/Users/marco/OneDrive - Caja Costarricense de Seguro Social/2025/Mantenimiento")
for path in root.iterdir():
    norm = unicodedata.normalize('NFKD', path.name).encode('ascii', 'ignore').decode().lower()
    if 'condiciones' in norm:
        print(path)
