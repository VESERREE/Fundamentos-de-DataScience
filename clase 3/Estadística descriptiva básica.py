"""
3. Estadística descriptiva básica
---------------------------------
- Calcula el promedio, la mediana y la moda del ataque de todos los Pokémon. ✅
- ¿Cuál es el Pokémon con mayor defensa? ¿Y el de menor velocidad? ✅
- ¿Cuántos Pokémon tienen dos tipos? ✅
- Calcula el rango y la desviación estándar de los PS (Puntos de Salud). ✅
"""

import pandas as pd

# Leer datos csv
df_csv = pd.read_csv("pokemon_primera_gen.csv")

# Promedio ataque
promedio_ataque = df_csv['Ataque'].mean()
print(f"\n El promedio de ataque de todos los pokemones es de",promedio_ataque.round(1))

# Mediana ataque
mediana_ataque = df_csv['Ataque'].median()
print(f"\n La mediana de todos los valores de ataque de los pokemones es",mediana_ataque)

# Moda ataque
moda_ataque = df_csv['Ataque'].mode()[0]
print(f"\n La moda de todos los valores de ataque de los pokemones es",moda_ataque)

# Pokemon con mayor defensa
mayor_defensa = df_csv.loc[df_csv['Defensa'].idxmax()]
print("\n El Pokémon con mayor defensa es:")
print(mayor_defensa,['Nombre', 'Tipo 1', 'Defensa'])

# Pokemon con menor velocidad
menor_velocidad = df_csv.loc[df_csv['Velocidad'].idxmin()]
print("\n El Pokémon con menor velocidad es:")
print(menor_velocidad,['Nombre', 'Tipo 1', 'Velocidad'])

# Pokemon con 2 tipos
pokemon_2_tipos = df_csv[df_csv["Tipo 2"].notnull()]
print("\n Pokémon con 2 tipos:",len(pokemon_2_tipos))

# Rango PS
rango_ps = df_csv['PS'].max() - df_csv['PS'].min()
print("\n El rango de los PS de los pokemones es", rango_ps)

# Desviacion PS
desviacion_PS = df_csv['PS'].std()
print("\n La desviación estándar de los PS de los pokemones es", desviacion_PS.round(1))