# Convencion para importar NumPy
import numpy as np

# Crear un array de NumPy desde una lista
lista_notas = [6.5, 7.0, 5.8, 4.9]
array_notas = np.array(lista_notas)
print(f"Las notas son: ",array_notas)
notas_finales_np = array_notas + 0.5
print(f"Las notas con 5 decimas mas son: ",notas_finales_np)