""" 
Una tienda online vende dos productos. Sus precios unitarios son precios = np.array([19990, 45500]) 
y las cantidades vendidas en un día fueron cantidades = np.array([10, 5]). Calcula e imprime:
a) El ingreso total por cada producto (precio * cantidad).
b) El ingreso total del día (suma de los ingresos por producto).
c) Si se aplica un descuento del 10% a todos los precios, ¿cuáles serían los nuevos precios?
"""
import numpy as np

precios = np.array([19990, 45500])
cantidad = np.array([10, 5])

# El ingreso total por cada producto (precio * cantidad)
ingreso_total_productos = precios*cantidad
print("Ingreso total de los productos es:", ingreso_total_productos)

# El ingreso total del día (suma de los ingresos por producto).
suma_ingresos = ingreso_total_productos.sum()
print("La suma total de los ingresos al final del dia es de:", suma_ingresos)

# Si se aplica un descuento del 10% a todos los precios, ¿cuáles serían los nuevos precios?
precio_desc = (precios*0.1)
print("Los precios son:", precio_desc) 