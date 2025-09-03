# Calcula el promedio de notas de cada estudiante y determina quién tiene el promedio más alto y más bajo.
import pandas as pd
import numpy as np

# Importar datos
from datos_estudiantes import DATOS_ESTUDIANTES
from validador_datos import validar_datos_estudiantes

# Validar datos y obtener DataFrame limpio
datos_validos, df = validar_datos_estudiantes(DATOS_ESTUDIANTES)

# Solo proceder si los datos son válidos
if not datos_validos:
    print("No se puede proceder con el análisis debido a datos inválidos")
    exit()

print("\n=== ANÁLISIS DE ESTUDIANTES APROBADOS ===")

# Crear DataFrame
df = pd.DataFrame(DATOS_ESTUDIANTES)

# Calcular promedio
df['Promedio'] = df['Notas'].apply(np.mean)

# Función para calcular min y max
def calcular_min_max(df):
    prom_min = df.loc[df['Promedio'].idxmin()]
    prom_max = df.loc[df['Promedio'].idxmax()]
    return prom_min, prom_max

# Ver resultados
print(df[['Nombre', 'Promedio']].round(2))

# Mostrar min y max
prom_min, prom_max = calcular_min_max(df)
print(f"Promedio más bajo: {prom_min['Nombre']} | {prom_min['Promedio']:.2f}")
print(f"Promedio más alto: {prom_max['Nombre']} | {prom_max['Promedio']:.2f}")