#Datos
notas_curso = [4.8, 6.2, 5.5, 3.9, 7.0, 4.1, 5.8, 6.0, 3.5, 5.2, 6.8, 2.9, 4.0, 4.0, 6.5]

tramo1 = []
tramo2 = []
tramo3 = []

for nota in notas_curso:
    if (nota < 4.0):
        tramo1.append(nota)
    elif (nota >= 4.0 and nota < 6.0):
        tramo2.append(nota)
    elif (nota >= 6.0):
        tramo3.append(nota)
# Promedio tramo reprobados        
promedio1 = sum(tramo1)/len(tramo1)

# Porcentaje tramo reprobados
porcentaje1 = (len(tramo1)/len(notas_curso))*100

# Promedio tramo aprobados y no destacados
promedio2 = sum(tramo2)/len(tramo2)

# Porcentaje tramo aprobados y no destacados
porcentaje2 = (len(tramo2)/len(notas_curso))*100

# Promedio tramo destacados
promedio3 = sum(tramo3)/len(tramo3)

# Porcentaje tramo destacados
porcentaje3 = (len(tramo3)/len(notas_curso))*100

# Print tramo reprobados
print (f"TRAMO REPROBADOS")
print (f"La cantidad de reprobados son: ", len(tramo1))
print (f"Las notas de este tramo son: ", tramo1)
print (f"El promedio entre los reprobados es: ", round(promedio1, 1))
print (f"El % respecto al total de alumnos es: ", porcentaje1, "%")

# Print tramo aprobados
print (f"TRAMO APROBADOS Y NO DESTACADOS")
print (f"La cantidad de aprobados y no destacados son: ", len(tramo2))
print (f"Las notas de este tramo son: ", tramo2)
print (f"El promedio entre los aprobados y  no destacados es: ", round(promedio2, 1))
print (f"El % respecto al total de alumnos es: ", round(porcentaje2, 1), "%")

# Print tramo destacados
print (f"TRAMO DESTACADOS")
print (f"La cantidad de destacados son: ", len(tramo3))
print (f"Las notas de este tramo son: ", tramo3)
print (f"El promedio entre los destacados es: ", round(promedio3, 1))
print (f"El % respecto al total de alumnos es: ", round(porcentaje3, 1), "%")
