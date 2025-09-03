# A partir del array de notas notas = np.array([4.5, 6.2, 3.9, 7.0, 5.5, 2.1]), 
# calcula e imprime el promedio, la desviación estándar, la nota máxima y la nota mínima.
"""
                Proceso:
                1. Crear el array `notas`.
                2. Utilizar los métodos del array: `.mean()`, `.std()`, `.max()`, `.min()`.
"""
import numpy as np
notas = np.array([4.5, 6.2, 3.9, 7.0, 5.5, 2.1])

print("Promedio:", notas.mean())
print("Desviación Estándar:", notas.std())
print("Nota Máxima:", notas.max())
print("Nota Mínima:", notas.min())