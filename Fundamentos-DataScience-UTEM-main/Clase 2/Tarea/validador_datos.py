"""
Módulo para validación básica de datos de estudiantes
"""
import pandas as pd

def validar_datos_estudiantes(datos, mostrar_resultados=True):
    df = pd.DataFrame(datos)
    
    if mostrar_resultados:
        print("Verificando Datos")
    
    # 1. Verificar que no haya listas vacías
    estudiantes_sin_notas = df[df['Notas'].apply(lambda x: len(x) == 0)]
    if not estudiantes_sin_notas.empty:
        if mostrar_resultados:
            print(f"Corregir/Revisar: {len(estudiantes_sin_notas)} estudiantes sin notas")
        return False, df
    elif mostrar_resultados:
        print("Todos los estudiantes tienen notas")
    
    # 2. Verificar rango de notas (1.0 - 7.0)
    def verificar_rango_notas(notas):
        return all(1.0 <= nota <= 7.0 for nota in notas)
    
    estudiantes_notas_invalidas = df[~df['Notas'].apply(verificar_rango_notas)]
    if not estudiantes_notas_invalidas.empty:
        if mostrar_resultados:
            print(f"Corregir/Revisar: {len(estudiantes_notas_invalidas)} estudiantes con notas fuera de rango (1.0-7.0)")
        return False, df
    elif mostrar_resultados:
        print("Todas las notas están en el rango válido (1.0-7.0)")

    # 3. Verificar que no haya notas negativas
    def tiene_notas_negativas(notas):
        return any(nota < 0 for nota in notas)
    
    estudiantes_notas_negativas = df[df['Notas'].apply(tiene_notas_negativas)]
    if not estudiantes_notas_negativas.empty:
        if mostrar_resultados:
            print(f"ERROR: {len(estudiantes_notas_negativas)} estudiantes con notas negativas")
        return False, df
    elif mostrar_resultados:
        print("No hay notas negativas")

    # 4. Verificar cantidad de notas por estudiante
    def verificar_cantidad_notas(notas):
        return len(notas) == 3
    
    estudiantes_notas_incompletas = df[~df['Notas'].apply(verificar_cantidad_notas)]
    if not estudiantes_notas_incompletas.empty:
        if mostrar_resultados:
            print(f"Corregir/Revisar: {len(estudiantes_notas_incompletas)} estudiantes con cantidad incorrecta de notas")
        return False, df
    elif mostrar_resultados:
        print("Todos los estudiantes tienen exactamente 3 notas")

    if mostrar_resultados:
        print("Datos validados correctamente")

    return True, df
