'''
Ejercicio 5: Manipulación de Datos de Inventario
Tienes un DataFrame de Pandas llamado df_inventario con la siguiente información:

Codigo_Producto	Stock_Inicial	Unidades_Vendidas	Costo_Unitario
LAP-01	50	15	600000
MOU-03	120	80	10000
TEC-02	80	45	30000
MON-05	40	10	120000
En tu hoja, realiza lo siguiente:
a) Escribe el código para añadir una nueva columna llamada Stock_Final, calculada como Stock_Inicial - Unidades_Vendidas. Muestra cómo quedaría la tabla final.

b) Escribe el código para filtrar y mostrar solo los productos con un Stock_Final menor a 30 unidades.

c) Escribe el código para calcular el valor total del inventario vendido, que sería la suma de (Unidades_Vendidas * Costo_Unitario).
'''
import pandas as pd
# Datos de inventario
df_inventario = pd.DataFrame({
    'Codigo_Producto': ['LAP-01', 'MOU-03', 'TEC-02', 'MON-05'],
    'Stock_Inicial': [50, 120, 80, 40],
    'Unidades_Vendidas': [15, 80, 45, 10],
    'Costo_Unitario': [600000, 10000, 30000, 120000]
})
# a) Añadir columna Stock_Final
df_inventario['Stock_Final'] = df_inventario['Stock_Inicial'] - df_inventario['Unidades_Vendidas']
print("Tabla con Stock_Final:\n", df_inventario)

# b) Filtrar productos con Stock_Final < 30
productos_bajo_stock = df_inventario[df_inventario['Stock_Final'] < 30]
print("Productos con Stock_Final < 30:\n", productos_bajo_stock)

# c) Calcular valor total del inventario vendido
valor_total_vendido = (df_inventario['Unidades_Vendidas'] * df_inventario['Costo_Unitario']).sum()
print("Valor total del inventario vendido:", valor_total_vendido)