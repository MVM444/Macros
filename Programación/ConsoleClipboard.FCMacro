#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script externo para leer el archivo de log de FreeCAD y copiar
las lineas que aparecieron en los ultimos 3 segundos de la ultima linea.
Se evita la interaccion directa con FreeCAD (GUI o macros internas),
asi no ocurre el Access Violation.
"""

import os
import sys
import pyperclip  # pip install pyperclip

# Ajusta esta ruta segun donde se ubique tu FreeCAD.log
# O configura manualmente la ruta si la sabes.
LOG_PATH = os.path.expanduser("~") + "/AppData/Roaming/FreeCAD/FreeCAD.log"  # Ejemplo en Windows

def parse_line_time(line):
    """
    Extrae 'HH:MM:SS' del inicio de la linea (posiciones [0:8]) y lo convierte
    a segundos del dia (ej: '07:54:40' -> 7*3600 + 54*60 + 40). Si falla,
    devuelve None.
    """
    if len(line) < 8:
        return None
    # Esperamos formato "HH:MM:SS" en [0:8]
    if line[2] != ':' or line[5] != ':':
        return None
    try:
        hh = int(line[0:2])
        mm = int(line[3:5])
        ss = int(line[6:8])
        return hh*3600 + mm*60 + ss
    except:
        return None

def copy_recent_messages_3sec_from_log(log_path):
    """
    Lee el archivo 'log_path', detecta la hora HH:MM:SS de la ultima linea,
    y toma las lineas que tengan hora >= (hora_ultima - 3).
    Luego las copia al portapapeles.
    """
    if not os.path.isfile(log_path):
        print("[Error] No se encontro el archivo de log:", log_path)
        return

    # Leemos todo el log
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.read().split('\n')

    if not lines:
        print("[Info] El log esta vacio.")
        return

    # Buscamos la ultima linea no vacia
    idx_last = len(lines) - 1
    while idx_last >= 0 and not lines[idx_last].strip():
        idx_last -= 1
    if idx_last < 0:
        print("[Info] No hay lineas no vacias en el log.")
        return

    last_line = lines[idx_last]
    last_line_time = parse_line_time(last_line)
    if last_line_time is None:
        # Si la ultima linea no tiene formato HH:MM:SS, copiamos solo esa linea
        print("[Info] La ultima linea no tiene HH:MM:SS. Se copia solo esa linea.")
        last_line_time = 0  # Forzamos a incluirla
    threshold = last_line_time - 3

    # Recorremos desde la ultima hasta la primera
    collected = []
    for i in range(idx_last, -1, -1):
        lt = parse_line_time(lines[i])
        # Si la linea tiene hora y es anterior al threshold => paramos
        if lt is not None and lt < threshold:
            break
        # De lo contrario, la incluimos
        collected.append(lines[i])

    # collected quedo de mas reciente a mas antigua. La invertimos
    collected.reverse()

    # Unimos y copiamos al portapapeles
    result_text = "\n".join(collected)
    pyperclip.copy(result_text)

    print("[OK] Se han copiado las lineas recientes al portapapeles:")
    print("---------------------------------------------------------")
    print(result_text)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    # Puedes pasar la ruta del log como argumento, o usar la que esta en LOG_PATH
    if len(sys.argv) > 1:
        LOG_PATH = sys.argv[1]

    copy_recent_messages_3sec_from_log(LOG_PATH)
