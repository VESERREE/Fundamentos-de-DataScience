"""
7. Análisis exploratorio (EDA)
------------------------------
- ¿Existen tipos de Pokémon que tienden a tener mayor ataque o defensa? Justifica con estadísticas. ✅
- ¿Hay correlación entre ataque y velocidad? Calcula el coeficiente de correlación. ✅
- ¿Qué tan dispersos están los PS dentro de cada tipo? (compara la desviación estándar de PS por tipo) ✅
- Identifica posibles outliers en los valores de ataque y PS usando boxplots. ✅
"""


import pandas as pd
import matplotlib.pyplot as plt

from leer_archivo_csv import obtener_pokemon_filtrados
df_csv = obtener_pokemon_filtrados()

def tendencias_ataque_defensa():
	estadisticas_tipo = df_csv.groupby('Tipo 1').agg({'Ataque': ['mean', 'median', 'std'], 'Defensa': ['mean', 'median', 'std']}).reset_index()
	estadisticas_tipo.columns = ['Tipo 1', 'Promedio Ataque', 'Mediana Ataque', 'Desviación Estándar Ataque', 'Promedio Defensa', 'Mediana Defensa', 'Desviación Estándar Defensa']
	estadisticas_tipo = round(estadisticas_tipo, 1)
	print("\nEstadísticas de Ataque y Defensa por Tipo 1:\n",estadisticas_tipo.to_string(index=False))
	print("\nTipos con mayor promedio de ataque:\n",estadisticas_tipo.sort_values(by='Promedio Ataque', ascending=False).head(3).to_string(index=False))
	print("\nTipos con mayor promedio de defensa:\n",estadisticas_tipo.sort_values(by='Promedio Defensa', ascending=False).head(3).to_string(index=False))
	print("\nCon esto se comprueba que existen tipos de pokemones que tienden a tener mayor ataque o defensa basándonos en los promedios.\n")

def correlacion_ataque_velocidad():
	correlacion = df_csv['Ataque'].corr(df_csv['Velocidad'])
	correlacion = round(correlacion, 2)
	print(f"\nLa correlación entre ataque y velocidad es: {correlacion}")
	print("Con esta correlacion se puede decir que hay una correlación positiva baja entre ataque y velocidad")
	print("Esto indica que a medida que el ataque aumenta, la velocidad tiende a aumentar ligeramente, pero la relación no es muy fuerte.\n")

def dispersion_ps_tipo():
	dispersion_ps = df_csv.groupby('Tipo 1')['PS'].agg(['mean', 'std']).reset_index()
	dispersion_ps.columns = ['Tipo 1', 'Promedio PS', 'Desviación Estándar PS']
	dispersion_ps = round(dispersion_ps, 1)
	print("Dispersión de PS por Tipo 1:\n",dispersion_ps.to_string(index=False))
	print("\nTipos con mayor desviación estándar de PS:\n")
	print(dispersion_ps.sort_values(by='Desviación Estándar PS', ascending=False).head(3).to_string(index=False))
	print("\nUna mayor desviación estándar indica que los PS de los pokemones de ese tipo están más dispersos alrededor del promedio.\n")

def boxplot_outliers():
	print("Los boxplots muestran la distribución de los valores de ataque y PS, incluyendo la mediana, los cuartiles y los posibles outliers (puntos fuera de los bigotes del boxplot).")
	print("Los outliers son valores atípicos que se encuentran significativamente alejados del resto de los datos.")
	print("Estos outliers pueden indicar pokemones con características inusuales en términos de ataque o PS.\n")
	plt.figure(figsize=(12, 6))
	plt.subplot(1, 2, 1)
	plt.boxplot(df_csv['Ataque'])
	plt.title('Boxplot de Ataque')
	plt.ylabel('Ataque')
	plt.subplot(1, 2, 2)
	plt.boxplot(df_csv['PS'])
	plt.title('Boxplot de PS')
	plt.ylabel('PS')
	plt.show()


def menu():
	while True:
		print("\nMenú de Análisis Exploratorio\n")
		print("1. Estadísticas de Ataque y Defensa por Tipo")
		print("2. Correlación Ataque vs Velocidad")
		print("3. Dispersión de PS por Tipo")
		print("4. Boxplot de Ataque y PS (outliers)")
		print("0. Salir")
		opcion = input("Elige una opción: ")
		if opcion == '1':
			tendencias_ataque_defensa()
		elif opcion == '2':
			correlacion_ataque_velocidad()
		elif opcion == '3':
			dispersion_ps_tipo()
		elif opcion == '4':
			boxplot_outliers()
		elif opcion == '0':
			print("Saliendo...")
			break
		else:
			print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
	menu()