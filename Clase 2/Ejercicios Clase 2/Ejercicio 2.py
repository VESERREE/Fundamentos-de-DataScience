# Crea una matriz de 3x3 con números del 1 al 9. A partir de ella, extrae:
# a) El número en la segunda fila, tercera columna (el 6).
# b) La segunda fila completa.
# c) La tercera columna completa.
# Proceso:
# 1. Crear la matriz usando `np.arange(1, 10).reshape(3, 3)`.
# 2. Para (a), usar indexación `matriz[1, 2]`.
# 3. Para (b), usar slicing `matriz[1, :]` o `matriz[1]`.
# 4. Para (c), usar slicing `matriz[:, 2]`.

import numpy as np

matriz = np.arange(1, 10).reshape(3, 3)
print ("Matriz original: \n", matriz)

# a) Elemento especifico
elemento = matriz[1, 2]
print ("Elemento en la fila 2, columna 3: \n", elemento)

# b) Segunda fila
fila_2 = matriz[1, :]
print ("Segunda fila completa: \n", fila_2)

# c) Tercera columna
columna_3 = matriz[:, 2]
print ("Tercera columna completa: \n", columna_3)