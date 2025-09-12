
import pandas as pd
import requests
import re

def obtener_pokemon_filtrados(ruta_csv="Clase 3/pokemon_primera_gen.csv", ruta_salida="Clase 3/pokemon_primera_gen_filtrado.csv"):
	# 1. Obtener la lista de pokemones de primera generación desde la PokeAPI
	url = "https://pokeapi.co/api/v2/generation/1/"
	response = requests.get(url)
	data = response.json()
	nombre_pokemones_1gen = [p['name'].lower() for p in data['pokemon_species']]


	# 2. Leer datos csv

	df_csv = pd.read_csv(ruta_csv)

	# VALIDACIONES
	# Eliminar filas con valores vacíos en columnas obligatorias (excepto Tipo 2 ya que puede ser una columna vacia)
	obligatorias = ['Nombre', 'Tipo 1', 'Ataque', 'Defensa', 'Velocidad', 'PS']
	vacios = df_csv[df_csv[obligatorias].isnull().any(axis=1)]
	if not vacios.empty:
		print("Advertencia: Se encontraron registros con casillas vacías en columnas obligatorias. Estos registros serán descartados.")
		print(vacios[['Nombre', 'Tipo 1']].to_dict('records'))
	df_csv = df_csv.dropna(subset=obligatorias)

	# Validar que el nombre solo tenga letras y espacios

	def nombre_valido(nombre):
		# Permitir letras, espacios, comillas simples, puntos, guiones y símbolos de género
		patron = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ '\.♀♂-]+$"
		if pd.isnull(nombre) or str(nombre).strip() == "":
			return False
		return bool(re.match(patron, str(nombre)))

	nombres_invalidos = df_csv[~df_csv['Nombre'].apply(nombre_valido)]['Nombre']
	if not nombres_invalidos.empty:
		print("Advertencia: Se encontraron nombres inválidos en el archivo CSV. Estos registros serán descartados.")
		print(nombres_invalidos.to_list())
	df_csv = df_csv[df_csv['Nombre'].apply(nombre_valido)]
	df_csv['Nombre'] = df_csv['Nombre'].str.lower()
	df_filtrado = df_csv[df_csv['Nombre'].isin(nombre_pokemones_1gen)]

	# 3. Adaptar nombres especiales para coincidir con la PokeAPI
	df_csv['Nombre'] = df_csv['Nombre'].replace({
		'nidoran♀': 'nidoran-f',
		'nidoran♂': 'nidoran-m'
	})
	df_csv['Nombre'] = df_csv['Nombre'].str.lower()
	df_filtrado = df_csv[df_csv['Nombre'].isin(nombre_pokemones_1gen)]

	# Corrección de tipos para casos especiales primera generación
	for nombre in ["clefairy", "clefable", "jigglypuff", "wigglytuff"]:
		df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 1'] = "Normal"
		df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 2'] = ""

	for nombre in ["magnemite", "magneton"]:
		df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 1'] = "Eléctrico"
		df_filtrado.loc[df_filtrado['Nombre'] == nombre, 'Tipo 2'] = ""

	# Filtramos por solo los tipos de la primera generación
	tipos_1gen = [
		"Bicho", "Dragón", "Eléctrico", "Lucha", "Fuego", "Volador", "Fantasma",
		"Tierra", "Hielo", "Normal", "Planta", "Veneno", "Psíquico", "Roca", "Agua"
	]
	df_filtrado = df_filtrado[df_filtrado['Tipo 1'].isin(tipos_1gen)]

	# 4. Guardar el nuevo archivo CSV
	df_filtrado.to_csv(ruta_salida, index=False)
	return df_filtrado

# Si se ejecuta directamente se va a crear el CSV filtrado
if __name__ == "__main__":
	obtener_pokemon_filtrados()