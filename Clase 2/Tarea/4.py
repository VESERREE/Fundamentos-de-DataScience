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
