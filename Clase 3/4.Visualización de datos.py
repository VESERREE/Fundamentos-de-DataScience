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

# Leer datos csv
df_csv = pd.read_csv("Clase 3/pokemon_primera_gen.csv")
print(df_csv)

# Crear histograma de ataque
plt.hist(df_csv['Ataque'], bins=15, color='skyblue', edgecolor='black')
plt.title('Histograma de ataque')
plt.xlabel('Ataque')
plt.ylabel('Cantidad')
plt.show()

# Gráfico de dispersión entre ataque y velocidad
plt.scatter(df_csv['Ataque'], df_csv['Velocidad'], color='orange', edgecolor='black')
plt.title('Gráfico de dispersión entre ataque y velocidad')
plt.xlabel('Ataque')
plt.ylabel('Velocidad')
plt.show()

# Boxplot de PS por tipo principal
plt.figure(figsize=(12, 6))
df_csv.boxplot(column='PS', by='Tipo 1', grid=False)
plt.title('Boxplot de PS por tipo 1')
plt.xlabel('Tipo 1')
plt.ylabel('PS')
plt.show()

# Diagrama de violín de Defensa por tipo principal
plt.figure(figsize=(12, 6))
sns.violinplot(x='Tipo 1', y='Defensa', data=df_csv)
plt.title('Diagrama de violín de Defensa por tipo 1')
plt.xlabel('Tipo 1')
plt.ylabel('Defensa')
plt.show()