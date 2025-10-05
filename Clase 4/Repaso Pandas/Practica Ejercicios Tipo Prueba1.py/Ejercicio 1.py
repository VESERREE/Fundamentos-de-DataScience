'''
Ejercicio 1: Análisis de Datos de Clientes
Tienes un DataFrame de Pandas llamado df_clientes con la siguiente información:

Nombre	Edad	Ciudad	Compras
Ana	28	Santiago	5
Luis	35	Valparaíso	2
Sofía	22	Concepción	7
Pedro	41	Santiago	1
En tu hoja, realiza lo siguiente:
a Escribe el código para filtrar y mostrar solo los clientes de Santiago que hayan realizado más de 3 compras.

b Escribe el código para calcular la edad promedio de los clientes de cada ciudad.

c Escribe el código para añadir una columna llamada Segmento que diga "Frecuente" si las compras son 5 o más, y "Ocasional" en caso contrario.
'''
import pandas as pd

# Datos de clientes
df_clientes = pd.DataFrame({
    'Nombre': ['Ana', 'Luis', 'Sofia', 'Pedro'],
    'Edad': [28, 35, 22, 41],
    'Ciudad': ['Santiago', 'Valparaíso', 'Concepción', 'Santiago'],
    'Compras': [5, 2, 7, 1]
})

# a) Filtrar clientes de Santiago con más de 3 compras
Only_Santiago = df_clientes[(df_clientes['Ciudad'] == 'Santiago') & (df_clientes['Compras'] > 3)]
print(Only_Santiago)

# b) Calcular la edad promedio de los clientes de cada ciudad
Edad_promedio = df_clientes.groupby('Ciudad')['Edad'].mean()
print("Edad promedio por ciudad:\n", Edad_promedio)

# c) Añadir columna Segmento
def asignar_segmento(compras):
    if compras >= 5:
        return 'Frecuente'
    else:
        return 'Ocasional'
df_clientes['Segmento'] = df_clientes['Compras'].apply(asignar_segmento)
print(df_clientes)