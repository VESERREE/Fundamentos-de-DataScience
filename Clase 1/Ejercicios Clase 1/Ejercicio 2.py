#Datos
notas_curso = [4.8, 6.2, 5.5, 3.9, 7.0, 4.1, 5.8, 6.0, 3.5, 5.2]

sobre5 = 0

maximo = max(notas_curso)
minimo = min(notas_curso)
for nota in notas_curso:
    if (nota > 5.0):
        sobre5 += 1
promedio = sum(notas_curso) / len(notas_curso)

print(f"El promedio es: ",(round(promedio, 1)))
print(f"Los estudiantes sobre 5.0 son: ",sobre5)
print (f"La nota mayor es: ",maximo)
print (f"La nota menor es: ",minimo)