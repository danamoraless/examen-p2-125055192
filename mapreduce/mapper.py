#!/usr/bin/env python3
import sys

for linea in sys.stdin:
    partes = linea.strip().split(",")
    # Ignora encabezado y lineas mal formadas
    if len(partes) != 8 or partes[0] == "id":
        continue
    try:
        tienda = partes[2]
        ingreso = int(partes[5]) * float(partes[6])
    except ValueError:
        continue
    print(f"{tienda}\t{ingreso}\t1")
