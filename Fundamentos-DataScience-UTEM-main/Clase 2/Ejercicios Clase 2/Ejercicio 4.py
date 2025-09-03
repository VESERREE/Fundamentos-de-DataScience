# Dado el array de notas del ejercicio anterior, selecciona e imprime únicamente las notas aprobatorias (mayores o iguales a 4.0).
"""
                Proceso:
                1. Crear el array `notas`.
                2. Crear una "máscara booleana" con la condición `notas >= 4.0`. Esto creará un nuevo array de `True`/`False`.
                3. Usar esta máscara para indexar el array original: `notas[mascara]`.
"""
import numpy as np
notas = np.array([4.5, 6.2, 3.9, 7.0, 5.5, 2.1])
mascara_aprobados = notas >= 4.0
notas_aprobados = notas[mascara_aprobados]

print("Notas originales: ", notas)
print("Notas aprobadas: ", notas_aprobados)