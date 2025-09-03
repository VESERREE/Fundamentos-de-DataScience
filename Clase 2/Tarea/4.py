# ¿Qué porcentaje de estudiantes tiene al menos una nota bajo 4.0? 

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

def reprobrado_seguro(notas_df):
            if isinstance(notas_df, list) and len(notas_df) > 0 and np.any(np.array(notas_df) < 4.0): 
                # Verifica que notas sea una lista, que no esté vacía y que alguna nota sea menor a 4.0
                return 'Reprobado'
            else:
                return "Aprobado"
                
df_completo['reprobados'] = df_completo['Notas'].apply(reprobrado_seguro)
reprobados = np.sum(df_completo['reprobados'] == 'Reprobado')
porcentaje_reprobados = pd.Series(reprobados / len(df_completo) * 100)
porcentaje_reprobados = round(porcentaje_reprobados, 1)
print(f"Porcentaje de estudiantes que reprobaron alguna asignatura: {porcentaje_reprobados.to_string(index=False)}%")
print