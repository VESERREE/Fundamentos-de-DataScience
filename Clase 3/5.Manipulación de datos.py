"""
5. Manipulación de datos
------------------------
- Crea una nueva columna llamada "Poder Total" que sea la suma de ataque, defensa, velocidad y PS. ✅
- Ordena el DataFrame por "Poder Total" de mayor a menor. ✅
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from leer_archivo_csv import obtener_pokemon_filtrados
# Obtener el DataFrame filtrado
df_csv = obtener_pokemon_filtrados()

# Crear nueva columna "Poder Total"
df_csv['Poder Total'] = df_csv[['Ataque', 'Defensa', 'Velocidad', 'PS']].sum(axis=1)

# Ordenar el DataFrame por "Poder Total" de mayor a menor
df_ordenado = df_csv.sort_values(by='Poder Total', ascending=False)
print(df_ordenado.to_string(index=False, columns=['Nombre', 'Poder Total']))