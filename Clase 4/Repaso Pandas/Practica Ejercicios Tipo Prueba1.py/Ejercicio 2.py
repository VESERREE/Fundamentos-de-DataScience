'''
Tienes una lista de diccionarios en Python llamada estudiantes:

estudiantes = [ {"nombre": "Ana", "notas": [6.5, 7.0, 5.8]}, {"nombre": "Luis", "notas": [4.2, 5.1, 6.0]}, {"nombre": "Sofía", "notas": [3.9, 4.0, 4.5]}, {"nombre": "Pedro", "notas": [5.5, 6.1, 5.9]} ]
En tu hoja, responde:
a) Escribe el código para calcular el promedio general de notas del curso.

b) Escribe el código para contar cuántos estudiantes aprobaron todas sus asignaturas (todas las notas >= 4.0).

c) Escribe el código para obtener la nota más frecuente (moda) considerando todas las notas de todos los estudiantes.
'''
import pandas as pd

estudiantes = [ {"nombre": "Ana", "notas": [6.5, 7.0, 5.8]}, 
               {"nombre": "Luis", "notas": [4.2, 5.1, 6.0]}, 
               {"nombre": "Sofía", "notas": [3.9, 4.0, 4.5]}, 
               {"nombre": "Pedro", "notas": [5.5, 6.1, 5.9]} ]
# Convertir la lista de diccionarios en un DataFrame
df_estudiantes = pd.DataFrame(estudiantes)

# a) Calcular el promedio general de notas del curso
df_estudiantes['promedio'] = df_estudiantes['notas'].apply(lambda x: sum(x)/len(x))
promedio_general = df_estudiantes['promedio'].mean()
print("Promedio general de notas del curso:", promedio_general)

# b) Contar cuántos estudiantes aprobaron todas sus asignaturas (todas las notas >= 4.0)
aprobados_todas = df_estudiantes['notas'].apply(lambda x: all(nota >= 4.0 for nota in x)).sum()
print("Cantidad de estudiantes que aprobaron todas sus asignaturas:", aprobados_todas)

# c) Obtener la nota más frecuente (moda)
notas_todas = df_estudiantes['notas'].explode().mode()
print("La nota más frecuente (moda) es:", notas_todas)