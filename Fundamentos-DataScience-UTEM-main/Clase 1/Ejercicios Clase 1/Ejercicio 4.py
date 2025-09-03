"""
Contexto:

Tienes una lista de estudiantes, cada uno representado por un diccionario con su nombre y una lista de notas. Ejemplo:

estudiantes = [
    {"nombre": "Ana", "notas": [6.5, 7.0, 5.8]},
    {"nombre": "Luis", "notas": [4.2, 5.1, 6.0]},
    {"nombre": "Sofía", "notas": [3.9, 4.0, 4.5]},
    # ... más estudiantes ...
]

Desafío:

Calcula el promedio de notas de cada estudiante y determina quién tiene el promedio más alto y más bajo. ✅

Cuenta cuántos estudiantes aprobaron todas sus asignaturas (todas las notas >= 4.0). ✅

¿Cuál es la nota más frecuente (moda) considerando todas las notas de todos los estudiantes? ✅

¿Qué porcentaje de estudiantes tiene al menos una nota bajo 4.0? ✅

Entrega un listado ordenado (de mayor a menor) de los estudiantes según su promedio. ✅
"""
import statistics

estudiantes = [
    {"nombre": "Ana", "notas": [6.5, 7.0, 5.8]},
    {"nombre": "Luis", "notas": [4.2, 5.1, 6.0]},
    {"nombre": "Sofía", "notas": [3.9, 4.0, 4.5]},
    {"nombre": "Martín", "notas": [5.5, 6.1, 6.8]},
    {"nombre": "Valentina", "notas": [6.9, 6.7, 7.0]},
    {"nombre": "Camila", "notas": [4.8, 5.2, 5.5]},
    {"nombre": "Diego", "notas": [3.5, 4.2, 4.0]},
    {"nombre": "Fernanda", "notas": [5.9, 6.0, 6.3]},
    {"nombre": "Ricardo", "notas": [4.0, 4.5, 4.8]},
    {"nombre": "Daniela", "notas": [6.3, 6.7, 6.9]},
    {"nombre": "Tomás", "notas": [2.9, 3.8, 4.1]},
    {"nombre": "Carolina", "notas": [5.0, 5.2, 5.6]},
    {"nombre": "Felipe", "notas": [6.8, 6.9, 7.0]},
    {"nombre": "Javiera", "notas": [3.6, 4.1, 4.0]},
    {"nombre": "Andrés", "notas": [4.5, 4.7, 5.1]},
    {"nombre": "Constanza", "notas": [5.7, 6.0, 5.8]},
    {"nombre": "Claudio", "notas": [6.2, 5.9, 6.4]},
    {"nombre": "Isidora", "notas": [4.1, 4.3, 4.0]},
    {"nombre": "Benjamín", "notas": [5.5, 5.8, 6.1]},
    {"nombre": "Catalina", "notas": [6.0, 6.2, 6.5]},
    {"nombre": "Matías", "notas": [3.5, 3.9, 4.0]},
    {"nombre": "Paula", "notas": [4.8, 5.0, 5.4]},
    {"nombre": "Ignacio", "notas": [6.9, 6.5, 6.8]},
    {"nombre": "Francisca", "notas": [4.2, 4.0, 4.4]},
    {"nombre": "Rodrigo", "notas": [5.9, 6.0, 6.3]},
    {"nombre": "María", "notas": [6.8, 7.0, 6.7]},
    {"nombre": "Pedro", "notas": [3.8, 4.0, 3.9]},
    {"nombre": "Josefina", "notas": [5.2, 5.4, 5.6]},
    {"nombre": "Cristóbal", "notas": [6.3, 6.5, 6.2]},
    {"nombre": "Rocío", "notas": [4.0, 4.2, 4.1]},
    {"nombre": "Sebastián", "notas": [6.6, 6.8, 7.0]},
    {"nombre": "Antonia", "notas": [3.7, 3.9, 4.0]},
    {"nombre": "Vicente", "notas": [4.9, 5.3, 5.6]},
    {"nombre": "Gabriela", "notas": [5.7, 6.0, 6.4]},
    {"nombre": "Álvaro", "notas": [6.8, 6.9, 7.0]}
]
promedios_estudiantes = []

# Calcula el promedio de notas de cada estudiante y determina quién tiene el promedio más alto y más bajo.

for notas in estudiantes:
    # Calculo de promedio por estudiante aproximado a un decimal
    promedio_estudiante = round((sum(notas["notas"])/len(notas["notas"])), 1)

    # Insertar cada promedio calculado en una nueva lista vacia
    promedios_estudiantes.append({"nombre": notas["nombre"], "promedio": promedio_estudiante})

# Definimos min y max de los promedios
minimo = min(promedios_estudiantes, key=lambda x: x['promedio'])
print(f"\nEl promedio mas bajo es: {minimo['nombre']} | {minimo['promedio']:.1f}")

maximo = max(promedios_estudiantes, key=lambda x: x["promedio"])
print(f"\nEl promedio mas alto es: {maximo['nombre']} | {maximo['promedio']:.1f}")

# Cuenta cuántos estudiantes aprobaron todas sus asignaturas (todas las notas >= 4.0).
estudiantes_aprobados = [
    estudiante["nombre"] for estudiante in estudiantes
    if all(nota >= 4.0 for nota in estudiante["notas"])
]
print(f"\nLos estudiantes aprobados son: {len(estudiantes_aprobados)} estudiantes")


# ¿Cuál es la nota más frecuente (moda) considerando todas las notas de todos los estudiantes?
all_notas = []
for estudiante in estudiantes:
    all_notas.extend(estudiante["notas"])

frecuencias = {}
for nota in all_notas:
    if nota in frecuencias:
        frecuencias[nota] += 1
    else:
        frecuencias[nota] = 1

moda = None
max_frecuencia = 0
for nota, frecuencia in frecuencias.items():
    if frecuencia > max_frecuencia:
        max_frecuencia = frecuencia
        moda = nota

print(f"\nLa nota más frecuente es: {moda} apareciendo {max_frecuencia} veces")

# ¿Qué porcentaje de estudiantes tiene al menos una nota bajo 4.0?
estudiantes_una_nota_baja = []
for estudiante in estudiantes:
    if any(nota < 4.0 for nota in estudiante["notas"]):
        estudiantes_una_nota_baja.append(estudiante["nombre"])
porcentaje = (len(estudiantes_una_nota_baja) / len(estudiantes)) * 100

print(f"\nPorcentaje de estudiantes con al menos una nota bajo 4.0: {porcentaje:.1f}%")

# Entrega un listado ordenado (de mayor a menor) de los estudiantes según su promedio.
estudiantes_ordenados = sorted(promedios_estudiantes, key=lambda estudiante: estudiante['promedio'], reverse=True)

print("\nLista de estudiantes ordenada por promedio:")
for estudiante in estudiantes_ordenados:
    print(f"Nombre: {estudiante['nombre']}, Promedio: {estudiante['promedio']:.1f}")