import os
import re
from unidecode import unidecode
import csv
import glob
import pandas as pd
import numpy as np
import sys

DIRECTORIO_DATOS = r'e:\Fundamentos-DataScience-UTEM-main\Trabajo\Código\Datos'

def normalizar_texto(texto):
    # Si no es string se retorna tal cual.
    if not isinstance(texto, str):
        return texto
    # Normalizamos cadena de texto.
    # Minusculas
    texto = texto.lower()
    # Sin tildes
    texto = unidecode(texto)
    # Espacios por guiones bajos
    texto = re.sub(r'\s+', '', texto)
    # Eliminamos comillas
    texto = texto.replace('"', '').replace("'", "")
    # Guiones por espacios
    texto = texto.replace('-', '')
    # Eliminar caracteres no alfanuméricos excepto guiones bajos
    texto = re.sub(r'[^a-z0-9_]', '', texto)
    # Retornar texto normalizado
    return texto

def normalizar_texto_header(texto, replace_char='_'):
    """
    Normaliza nombres de columna.

    - Convierte a minúsculas
    - Quita tildes
    - Elimina espacios
    - Reemplaza '-' por `replace_char` (por defecto '_')
    - Elimina caracteres no alfanuméricos excepto guión bajo
    """
    if not isinstance(texto, str):
        return texto
    texto = texto.lower()
    texto = unidecode(texto)
    texto = re.sub(r'\s+', '', texto)
    texto = texto.replace('-', replace_char)
    texto = re.sub(r'[^a-z0-9_]', '', texto)
    return texto

def normalizar_valor_quitar_guion(valor):
    """
    Elimina los caracteres - dentro de un valor manteniendo el resto del dato.

    - Si el valor no es string, se retorna tal cual.
    - Para strings, se eliminan todos los - y se hace strip().
    """
    # Si el valor es None, se retorna None.
    if valor is None:
        return valor
    # Si no es string se retorna tal cual.
    if not isinstance(valor, str):
        return valor
    # Eliminar comillas simples y dobles y luego guiones dentro del valor, mantener el resto
    v = valor.replace('"', '').replace("'", "")
    v = v.replace('-', '')
    # Retornar valor limpio
    return v.strip()

def limpiar_linea_csv(linea, normalizar_funcion):
    # Limpiamos cada celda de la línea usando la función de normalización creada.
    return [normalizar_funcion(n) for n in linea]

# Esta funcion esta pensada en base al formato de archivos que otorga el INE de Chile sobre el Censo 2024.
def limpiar_csv(ruta_original):

    try:
        # Verificar si el archivo está vacío
        if os.path.getsize(ruta_original) == 0:
            print(f"El archivo está vacío, no se puede limpiar.")
            return

        # Se crea la ruta del nuevo archivo limpio
        directorio, nombre_archivo = os.path.split(ruta_original)
        nombre_base, extension = os.path.splitext(nombre_archivo)
        nuevo_archivo_limpio = os.path.join(directorio, f"{nombre_base}_limpio{extension}")

        # Abrir el archivo original y el archivo limpio para poder escribir en él
        # Se usa 'with' para asegurar que los archivos se cierren correctamente
        # Se especifica el modo de apertura para cada archivo
        # 'r' para lectura en el archivo original y 'w' para escritura en el archivo limpio
        with open(ruta_original, 'r', encoding='utf-8') as f_in, open(nuevo_archivo_limpio, 'w', newline='', encoding='utf-8') as f_out:
            # Leer todas las líneas para poder omitir las del final
            lineas = f_in.readlines()
            
            # Omitir las primeras 3 líneas y las últimas 3
            lineas_a_procesar = lineas[3:-3]

            # Crear lectores y escritores CSV
            lector_csv = csv.reader(lineas_a_procesar)
            escritor_csv = csv.writer(f_out)

            # Leer y procesar la cabecera (usar función específica para cabeceras)
            cabecera = next(lector_csv)
            cabecera_limpia = limpiar_linea_csv(cabecera, normalizar_texto_header)
            escritor_csv.writerow(cabecera_limpia)

            # Procesar y escribir el resto de las filas (eliminar '-' dentro de valores, mantener dato)
            for fila in lector_csv:
                fila_limpia = limpiar_linea_csv(fila, normalizar_valor_quitar_guion)
                escritor_csv.writerow(fila_limpia)

        print("Archivo limpio creado con éxito.")

    except FileNotFoundError:
        print(f"No se encontró el archivo")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def unir_csvs(directorio_datos, archivo_salida_final):
    try:
        # Encontrar todos los archivos que terminan en '_limpio.csv'
        archivos_a_unir = glob.glob(os.path.join(directorio_datos, '*_limpio.csv'))
        
        if not archivos_a_unir:
            print("No se encontraron archivos limpios para unir.")
            return

        # Columnas comunes para la fusión
        columnas_clave = ['codigoregion', 'region', 'codigoprovincia', 'provincia', 'codigocomuna', 'comuna']
        
        # Leer el primer archivo para iniciar el DataFrame consolidado
        df_consolidado = None

        for i, ruta_archivo in enumerate(archivos_a_unir):
            try:
                df_actual = pd.read_csv(ruta_archivo,
                    # Especificar que las columnas clave se lean como strings
                    dtype={c: 'string' for c in columnas_clave})

                # Limpiar comillas dobles residuales en las columnas de texto
                columnas_texto = df_actual.select_dtypes(include=['object', 'string']).columns
                for col in columnas_texto:
                    df_actual[col] = df_actual[col].str.replace('"', '', regex=False)

                # Limpiar nombres de columnas por si acaso (reemplazar '-' por '_')
                df_actual.columns = [normalizar_texto_header(str(col)) for col in df_actual.columns]

                # Verificar que existan todas las columnas clave necesarias
                columnas_clave_presentes = [col for col in columnas_clave if col in df_actual.columns]
                if len(columnas_clave_presentes) != len(columnas_clave):
                    columnas_faltantes = [col for col in columnas_clave if col not in columnas_clave_presentes]
                    print(
                        f"Advertencia: El archivo {ruta_archivo} no contiene las columnas clave requeridas: {', '.join(columnas_faltantes)}. Se omitirá de la unión."
                    )
                    continue

                # Convertir columnas clave a string para evitar problemas en el merge
                for col in columnas_clave_presentes:
                    df_actual[col] = df_actual[col].astype(str)

                # Manejo de duplicados
                if df_actual.duplicated(subset=columnas_clave).any():
                    # agrega por suma en numéricos, first en el resto
                    num_cols = df_actual.select_dtypes(include=['number','Int64','float']).columns.difference(columnas_clave)
                    otras_cols = df_actual.columns.difference(num_cols.union(columnas_clave))
                    df_actual = (df_actual
                                 .groupby(columnas_clave, as_index=False)
                                 .agg({**{c:'sum' for c in num_cols},
                                       **{c:'first' for c in otras_cols}}))

                if df_consolidado is None:
                    df_consolidado = df_actual
                else:
                    # Seleccionar columnas a unir del df_actual evitando duplicados
                    columnas_existentes = set(df_consolidado.columns)
                    columnas_nuevas = [col for col in df_actual.columns if col not in columnas_existentes]
                    columnas_para_unir = columnas_clave_presentes + columnas_nuevas    
                    # Usar 'merge' para unir horizontalmente los datos
                    df_consolidado = pd.merge(
                        df_consolidado,
                        df_actual[columnas_para_unir],
                        on=columnas_clave_presentes,
                        how='outer'
                    )

            except pd.errors.EmptyDataError:
                print(f" El archivo {ruta_archivo} está vacío y será omitido.")
            except Exception as e:
                print(f"No se pudo procesar el archivo {ruta_archivo}." f" Error: {e}")

        if df_consolidado is None or df_consolidado.empty:
            print("No se pudieron leer datos de ningún archivo limpio para consolidar.")
            return

        # Guardar el DataFrame consolidado en un nuevo archivo CSV
        df_consolidado.to_csv(archivo_salida_final, index=False, encoding='utf-8')
        
        print(f"Archivo consolidado guardado en: {archivo_salida_final}")

    except Exception as e:
        print(f"Ocurrió un error durante la unión de archivos con pandas: {e}")


def _to_numeric(serie: pd.Series) -> pd.Series:
    valores = (
        serie.astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )
    valores = valores.replace({'': np.nan, 'nan': np.nan})
    return pd.to_numeric(valores, errors='coerce')


def _safe_division(numerador: pd.Series, denominador: pd.Series) -> pd.Series:
    den = denominador.replace({0: np.nan, 0.0: np.nan})
    resultado = numerador / den
    return resultado.replace([np.inf, -np.inf], np.nan)


def main():
    # Limpiar todos los archivos CSV en el directorio
    print(f"Buscando archivos en: {DIRECTORIO_DATOS}")
    archivos_originales = glob.glob(os.path.join(DIRECTORIO_DATOS, '*.csv'))
    
    # Excluir archivos que ya están limpios o son el consolidado
    archivos_a_limpiar = [f for f in archivos_originales if not f.endswith('_limpio.csv') and not f.endswith('consolidado_limpio.csv')]

    if not archivos_a_limpiar:
        print("No se encontraron nuevos archivos para limpiar.")
    else:
        for archivo in archivos_a_limpiar:
            limpiar_csv(archivo)

    # 2. Unir todos los archivos limpios en uno solo
    archivo_salida_final = os.path.join(DIRECTORIO_DATOS, 'consolidado_limpio.csv')
    print("\nUniendo archivos limpios")
    unir_csvs(DIRECTORIO_DATOS, archivo_salida_final)

if __name__ == '__main__':
    main()