"""
3. Estadística descriptiva básica
---------------------------------
- Calcula el promedio, la mediana y la moda del ataque de todos los Pokémon. ✅
- ¿Cuál es el Pokémon con mayor defensa? ¿Y el de menor velocidad? ✅
- ¿Cuántos Pokémon tienen dos tipos? ✅
- Calcula el rango y la desviación estándar de los PS (Puntos de Salud). ✅
"""

import pandas as pd

from leer_archivo_csv import obtener_pokemon_filtrados
# Obtener el DataFrame filtrado
df_csv = obtener_pokemon_filtrados()

def promedio_ataque():
	promedio_ataque = df_csv['Ataque'].mean()
	print(f"\n El promedio de ataque de todos los pokemones es de",round(promedio_ataque, 1))

def mediana_ataque():
	mediana_ataque = df_csv['Ataque'].median()
	print(f"\n La mediana de todos los valores de ataque de los pokemones es",mediana_ataque)

def moda_ataque():
	moda_ataque = df_csv['Ataque'].mode()[0]
	print(f"\n La moda de todos los valores de ataque de los pokemones es",moda_ataque)

def mayor_defensa():
	mayor_defensa = df_csv.loc[df_csv['Defensa'].idxmax()]
	print("\n El Pokémon con mayor defensa es:")
	print(mayor_defensa[['Nombre', 'Tipo 1', 'Defensa']])

def menor_velocidad():
	menor_velocidad = df_csv.loc[df_csv['Velocidad'].idxmin()]
	print("\n El Pokémon con menor velocidad es:")
	print(menor_velocidad[['Nombre', 'Tipo 1', 'Velocidad']])

def pokemones_dos_tipos():
	pokemon_2_tipos = df_csv[df_csv["Tipo 2"].notnull()]
	print("\n Pokémon con 2 tipos:",len(pokemon_2_tipos))

def rango_ps():
	rango_ps = df_csv['PS'].max() - df_csv['PS'].min()
	print("\n El rango de los PS de los pokemones es", rango_ps)

def desviacion_ps():
	desviacion_PS = df_csv['PS'].std()
	print("\n La desviación estándar de los PS de los pokemones es",round(desviacion_PS, 1))

def menu():
	opciones = {
		'1': promedio_ataque,
		'2': mediana_ataque,
		'3': moda_ataque,
		'4': mayor_defensa,
		'5': menor_velocidad,
		'6': pokemones_dos_tipos,
		'7': rango_ps,
		'8': desviacion_ps
	}
	while True:
		print("\n--- Menú Estadística Descriptiva Básica ---")
		print("1. Promedio de ataque")
		print("2. Mediana de ataque")
		print("3. Moda de ataque")
		print("4. Pokémon con mayor defensa")
		print("5. Pokémon con menor velocidad")
		print("6. Cantidad de Pokémon con 2 tipos")
		print("7. Rango de PS")
		print("8. Desviación estándar de PS")
		print("0. Salir")
		opcion = input("Elige una opción: ")
		if opcion == '0':
			print("Saliendo...")
			break
		funcion = opciones.get(opcion)
		if funcion:
			funcion()
		else:
			print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
	menu()