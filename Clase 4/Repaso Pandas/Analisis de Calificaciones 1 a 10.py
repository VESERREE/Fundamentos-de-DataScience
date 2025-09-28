import pandas as pd
import random

# Genera 100 números aleatorios entre 1 y 10
satisfaccion = [random.randint(1, 10) for _ in range(100)]

# DataFrame de los numeros
df_satisfaccion = pd.Series(satisfaccion)

# Mostrar notas
print("Las notas de satisfaccion son: ", df_satisfaccion)

# Media de calificaciones
media = df_satisfaccion.mean()
print("La media es: ", round(media, 1))

# Desviacion estandar
desviacion = df_satisfaccion.std()
print("La desviacion estandar es: ", round(desviacion, 1))

# Calificacion minima y maxima
calificacion_minima = df_satisfaccion.min()
print("La calificacion mas baja es: ", calificacion_minima)
calificacion_maxima = df_satisfaccion.max()
print("La calificacion mas alta es: ", calificacion_maxima)

# Cantidad mayor o igual a 8
Cantidad_Satisfecho = (df_satisfaccion >= 8).sum()
print("La cantidad de personas satisfechas (Calificacion mayor o igual a 8) es: ", Cantidad_Satisfecho)