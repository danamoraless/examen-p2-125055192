#!/usr/bin/env python3
import csv
from collections import defaultdict

suma = defaultdict(float)
cuenta = defaultdict(int)

with open("ventas_125055192.csv", newline="") as f:
    lector = csv.reader(f)
    next(lector)  # encabezado
    for fila in lector:
        if len(fila) != 8:
            continue
        try:
            ingreso = int(fila[5]) * float(fila[6])
        except ValueError:
            continue
        suma[fila[2]] += ingreso
        cuenta[fila[2]] += 1

for tienda in sorted(suma):
    print(f"{tienda}\t{suma[tienda] / cuenta[tienda]:.2f}")
