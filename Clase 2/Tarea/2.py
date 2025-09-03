# Cuenta cuántos estudiantes aprobaron todas sus asignaturas (todas las notas >= 4.0). 

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

# Expandimos las notas
notas_df = pd.DataFrame(df['Notas'].tolist(), columns=['Nota1', 'Nota2', 'Nota3'])
df_final = pd.concat([df, notas_df], axis=1)

# Verificamos los aprobados
aprobados = df_final[(df_final[['Nota1', 'Nota2', 'Nota3']] >= 4.0).all(axis=1)]

# Ver resultados
print(f"\nEstudiantes que aprobaron todas las asignaturas: {len(aprobados)}")
print(aprobados[['Nombre', 'Nota1', 'Nota2', 'Nota3']])
