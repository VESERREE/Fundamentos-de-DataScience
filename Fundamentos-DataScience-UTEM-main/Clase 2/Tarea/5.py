# Entrega un listado ordenado (de mayor a menor) de los estudiantes según su promedio.

import pandas as pd
import numpy as np

# Importar datos y validador
from datos_estudiantes import DATOS_ESTUDIANTES
from validador_datos import validar_datos_estudiantes

# Validar datos y obtener DataFrame limpio
datos_validos, df = validar_datos_estudiantes(DATOS_ESTUDIANTES)

# Solo proceder si los datos son válidos
if not datos_validos:
    print("No se puede proceder con el análisis debido a datos inválidos")
    exit()

print("\n=== ANÁLISIS DE ESTUDIANTES APROBADOS ===")

# Expandir las notas en columnas separadas
notas_df = pd.DataFrame(df['Notas'].tolist(), columns=['Nota1', 'Nota2', 'Nota3'])
df_completo = pd.concat([df, notas_df], axis=1)

# Crear DataFrame
df = pd.DataFrame(DATOS_ESTUDIANTES)

# Calcular promedio
df['Promedio'] = df['Notas'].apply(np.mean)

# Ordenar de mayor a menor
promedio_ordenado = df.sort_values(by='Promedio', ascending=False)

# Ver resultados
print("Lista de promedio ordenado: \n",promedio_ordenado[['Nombre', 'Promedio']].round(2))
