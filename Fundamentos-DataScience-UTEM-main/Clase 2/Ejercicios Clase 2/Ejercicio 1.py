# Dado un array de temperaturas en grados Celsius grados_c = np.array([0, 15, 25, 30, 100]), conviértelas a grados Fahrenheit usando 
# la fórmula $ F = C \times \frac{9}{5} + 32 $. Realiza la operación en una sola línea de código (vectorización).

import numpy as np
grados_c = np.array([0, 15, 25, 30, 100])
grados_f = grados_c * (9/5) + 32

print("Temperaturas en Celsius:", grados_c)
print("Temperaturas en Fahrenheit:", grados_f)