#!/usr/bin/env python3
import sys

actual = None
suma = 0.0
cuenta = 0

for linea in sys.stdin:
    try:
        tienda, ingreso, n = linea.strip().split("\t")
        ingreso = float(ingreso)
        n = int(n)
    except ValueError:
        continue
    if tienda != actual:
        if actual is not None:
            print(f"{actual}\t{suma / cuenta:.2f}")
        actual = tienda
        suma = 0.0
        cuenta = 0
    suma += ingreso
    cuenta += n

if actual is not None:
    print(f"{actual}\t{suma / cuenta:.2f}")
