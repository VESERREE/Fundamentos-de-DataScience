import pandas as pd
import requests


# 1. Obtener la lista de pokemones de primera generación desde la PokeAPI
url = "https://pokeapi.co/api/v2/generation/1/"
response = requests.get(url)
data = response.json()
nombre_pokemones_1gen = [p['name'].lower() for p in data['pokemon_species']]

# 2. Leer datos csv
df_csv = pd.read_csv("Clase 3/pokemon_primera_gen.csv")
print(df_csv)

# 3. Filtrar el DataFrame para que solo queden los de primera generación
df_csv['Nombre'] = df_csv['Nombre'].str.lower()
df_filtrado = df_csv[df_csv['Nombre'].isin(nombre_pokemones_1gen)]

# Corrección de tipos para casos especiales primera generación
for nombre in ["clefairy", "clefable", "jigglypuff", "wigglytuff"]: 
	df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 1'] = "Normal"
	df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 2'] = ""

for nombre in ["magnemite", "magneton"]:
	df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 1'] = "Eléctrico"
	df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 2'] = ""


# filtramos por solo los tipos de la primera generación
tipos_1gen = [
	"Bicho", "Dragón", "Eléctrico", "Lucha", "Fuego", "Volador", "Fantasma",
	"Tierra", "Hielo", "Normal", "Planta", "Veneno", "Psíquico", "Roca", "Agua"
]
df_filtrado = df_filtrado[df_filtrado['Tipo 1'].isin(tipos_1gen)]


# 4. Guardar el nuevo archivo CSV
df_filtrado.to_csv("Clase 3/pokemon_primera_gen_filtrado.csv", index=False)
print("Archivo filtrado creado con éxito.")
