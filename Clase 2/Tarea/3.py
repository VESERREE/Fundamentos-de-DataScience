# ¿Cuál es la nota más frecuente (moda) considerando todas las notas de todos los estudiantes?

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

# Usar melt para reestructurar los datos
notas_melted = pd.melt(
    df_completo, 
    id_vars=['Nombre', 'Edad'],
    value_vars=['Nota1', 'Nota2', 'Nota3'],
    var_name='Tipo_Nota',
    value_name='Nota'
)

# Calcular moda y frecuencias
moda = notas_melted['Nota'].mode()[0]
frecuencias = notas_melted['Nota'].value_counts()

# Ver resultados
print(f"Nota más frecuente (moda): {moda}")
print(f"Frecuencia: {frecuencias.iloc[0]} veces")
