import pandas as pd
from leer_archivo_csv import obtener_pokemon_filtrados
# Obtener el DataFrame filtrado
df_csv = obtener_pokemon_filtrados()

# Filtramos por tipos
tipo_fuego = df_csv[df_csv['Tipo 1'] == 'Fuego'][['Nombre', 'Tipo 1', 'Ataque', 'Velocidad']]
print(tipo_fuego.to_string(index=False))