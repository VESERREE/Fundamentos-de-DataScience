"""
6. Agrupamiento y análisis por grupo
-------------------------------------
- Calcula el promedio, la mediana y la desviación estándar de ataque por cada tipo principal (Tipo 1). ✅
- ¿Qué tipo tiene el mayor promedio de velocidad? ✅
- Para cada tipo principal, ¿cuál es el Pokémon con mayor y menor PS? ✅
"""

import pandas as pd

from leer_archivo_csv import obtener_pokemon_filtrados
# Obtener el DataFrame filtrado
df_csv = obtener_pokemon_filtrados()


def estadisticas_ataque_tipo():
	estadisticas_de_ataque = df_csv.groupby('Tipo 1')['Ataque'].agg(['mean', 'median', 'std']).reset_index()
	estadisticas_de_ataque = round(estadisticas_de_ataque, 1)
	estadisticas_de_ataque.columns = ['Tipo 1', 'Promedio ataque', 'Mediana ataque', 'Desviación estándar ataque']
	print("Estadísticas de ataque por Tipo 1:",estadisticas_de_ataque.to_string(index=False))

def tipo_mayor_promedio_velocidad():
	tipo_mayor_velocidad = df_csv.groupby('Tipo 1')['Velocidad'].mean().idxmax()
	promedio_mayor_velocidad = df_csv.groupby('Tipo 1')['Velocidad'].mean().max()
	promedio_mayor_velocidad = round(promedio_mayor_velocidad, 1)
	print(f"\nEl tipo con mayor promedio de velocidad es {tipo_mayor_velocidad} con un promedio de {promedio_mayor_velocidad}")

def pokemon_mayor_menor_ps():
	pokemon_mayor_ps = df_csv.loc[df_csv.groupby('Tipo 1')['PS'].idxmax()][['Tipo 1', 'Nombre', 'PS']]
	pokemon_menor_ps = df_csv.loc[df_csv.groupby('Tipo 1')['PS'].idxmin()][['Tipo 1', 'Nombre', 'PS']]
	print("\nPokémon con mayor PS por Tipo 1:\n")
	print(pokemon_mayor_ps.to_string(index=False))
	print("\nPokémon con menor PS por Tipo 1:\n")
	print(pokemon_menor_ps.to_string(index=False))

def menu():
	opciones = {
		'1': estadisticas_ataque_tipo,
		'2': tipo_mayor_promedio_velocidad,
		'3': pokemon_mayor_menor_ps
	}
	while True:
		print("\nMenú de Agrupamiento y Análisis por Grupo")
		print("1. Estadísticas de ataque por Tipo 1")
		print("2. Tipo con mayor promedio de velocidad")
		print("3. Pokémon con mayor y menor PS por Tipo 1")
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