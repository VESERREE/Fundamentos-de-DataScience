#Datos
notas_curso = [6.5, 7.0, 3.2, 4.9, 5.8, 2.1, 4.0]

suma = 0
aprobados = 0
for nota in notas_curso:
    if (nota > 3.9):
        aprobados += 1
        print (aprobados)
    suma += nota
promedio = suma / len(notas_curso)
print (f"El promedio es: ",(round(promedio, 1)))
print (f"La cantidad de alumnos aprobados es: ", aprobados)