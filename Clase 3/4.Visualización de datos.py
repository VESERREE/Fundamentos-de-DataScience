"""
4. Visualización de datos
-------------------------
- Haz un histograma de los valores de ataque. ✅
- Realiza un gráfico de dispersión entre ataque y velocidad. ✅
- Haz un boxplot de los PS por tipo principal (Tipo 1). ✅
- Grafica la distribución de la defensa usando un diagrama de violín. ✅
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from leer_archivo_csv import obtener_pokemon_filtrados
# Obtener el DataFrame filtrado
df_csv = obtener_pokemon_filtrados()


def mostrar_histograma():
	plt.hist(df_csv['Ataque'], bins=15, color='skyblue', edgecolor='black')
	plt.title('Histograma de ataque')
	plt.xlabel('Ataque')
	plt.ylabel('Cantidad')
	plt.show()

def mostrar_dispersion():
	plt.scatter(df_csv['Ataque'], df_csv['Velocidad'], color='orange', edgecolor='black')
	plt.title('Gráfico de dispersión entre ataque y velocidad')
	plt.xlabel('Ataque')
	plt.ylabel('Velocidad')
	plt.show()

def mostrar_boxplot():
	plt.figure(figsize=(12, 6))
	df_csv.boxplot(column='PS', by='Tipo 1', grid=False)
	plt.title('Boxplot de PS por tipo 1')
	plt.xlabel('Tipo 1')
	plt.ylabel('PS')
	plt.show()

def mostrar_violin():
	plt.figure(figsize=(12, 6))
	sns.violinplot(x='Tipo 1', y='Defensa', data=df_csv)
	plt.title('Diagrama de violín de Defensa por tipo 1')
	plt.xlabel('Tipo 1')
	plt.ylabel('Defensa')
	plt.show()

def menu():
	opciones = {
		'1': mostrar_histograma,
		'2': mostrar_dispersion,
		'3': mostrar_boxplot,
		'4': mostrar_violin
	}
	while True:
		print("\n--- Menú de Visualización de Datos ---")
		print("1. Histograma de Ataque")
		print("2. Dispersión Ataque vs Velocidad")
		print("3. Boxplot de PS por Tipo 1")
		print("4. Diagrama de violín de Defensa")
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