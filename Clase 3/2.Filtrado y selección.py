import pandas as pd

# Leer datos csv
df_csv = pd.read_csv("Clase 3/pokemon_primera_gen.csv")

# Filtramos por tipos
tipo_fuego = df_csv[df_csv['Tipo 1'] == 'Fuego'][['Nombre', 'Tipo 1', 'Ataque', 'Velocidad']]
print(tipo_fuego)