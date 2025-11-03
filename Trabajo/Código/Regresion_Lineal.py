import os
import numpy as np
import pandas as pd
from Limpieza import _safe_division, _to_numeric
from Graficos import graficar_regresion_lineal
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt 

def preparar_metricas(df: pd.DataFrame) -> pd.DataFrame:
    # Creamos una copia para no modificar el original
    df_local = df.copy()

    # Definimos las columnas necesarias
    columnas_base = [
        'viviendasparticularesocupadasconmoradorespresentes',
        'arrendadaconcontrato',
        'arrendadasincontrato',
        'mediaguamejoraviviendadeemergenciaranchoochoza',
        'viviendascon1hogar',
        'viviendascon2hogares',
        'viviendascon3hogares',
        'viviendascon4omashogares',
        'poblacioncensada',
        'ocupadadehecho',
        'hogarescensados',
    ]

    # Definimos las columnas de dormitorios
    columnas_dorm = [
        '0dormitorios',
        '1dormitorio',
        '2dormitorios',
        '3dormitorios',
        '4dormitorios',
        '5dormitorios',
        '6omasdormitorios',
    ]

    # Verificamos que todas las columnas necesarias estén presentes
    faltantes = [col for col in columnas_base + columnas_dorm if col not in df_local.columns]
    if faltantes:
        # Lanzamos un error si faltan columnas
        raise KeyError(f'Faltan columnas necesarias en el DataFrame: {faltantes}')
    
    # Convertimos las columnas a numéricas
    # Para evitar problemas en cálculos posteriores
    columnas_numericas = columnas_base + columnas_dorm
    # Recorremos y convertimos
    for columna in columnas_numericas:
        # Convertimos a numérico y llenamos NaN con 0.0
        df_local[columna] = _to_numeric(df_local[columna]).fillna(0.0)

    # Calculamos las métricas específicas
    viviendas_ocupadas = df_local['viviendasparticularesocupadasconmoradorespresentes']

    # Calculamos el total de hogares
    # Multiplicando por el número de hogares correspondiente
    total_hogares = (
        df_local['viviendascon1hogar'] * 1
        + df_local['viviendascon2hogares'] * 2
        + df_local['viviendascon3hogares'] * 3
        + df_local['viviendascon4omashogares'] * 4
    )
    # Definimos la variable objetivo
    df_local['TARGET_HOGARES_X_VIVIENDA'] = _safe_division(total_hogares, viviendas_ocupadas)

    # Pesos dormitorios para calcular promedio
    pesos_dorm = [0, 1, 2, 3, 4, 5, 6]
    # Calculamos el promedio de dormitorios
    total_dormitorios = pd.Series(0.0, index=df_local.index)
    # Sumamos el total ponderado de dormitorios
    for col, peso in zip(columnas_dorm, pesos_dorm):
        # Multiplicamos la columna de dormitorios por su peso
        total_dormitorios = total_dormitorios.add(df_local[col] * peso, fill_value=0.0)
    # Asignamos la métrica calculada
    df_local['FEATURE_DORMITORIOS_PROM'] = _safe_division(total_dormitorios, viviendas_ocupadas)

    # Calculamos la tenencia de arriendo con contrato y sin contrato
    total_arriendo = df_local['arrendadaconcontrato'] + df_local['arrendadasincontrato']
    # Asignamos la métrica calculada
    df_local['FEATURE_TENENCIA_ARRIENDO'] = _safe_division(total_arriendo, viviendas_ocupadas)

    # Calculamos la vulnerabilidad de la vivienda con respecto a viviendas de emergencia
    vulnerables = df_local['mediaguamejoraviviendadeemergenciaranchoochoza']
    # Asignamos la métrica calculada
    df_local['FEATURE_VIVIENDA_VULNERABLE'] = _safe_division(vulnerables, viviendas_ocupadas)

    # Definimos la variable objetivo y la asignamos
    df_local['FEATURE_DENSIDAD_POBLACIONAL'] = _safe_division(df_local['poblacioncensada'], df_local['viviendasparticularesocupadasconmoradorespresentes'])

    # Definimos la variable objetivo y la asignamos
    df_local['FEATURE_VULNERABILIDAD_TENENCIA'] = _safe_division(df_local['ocupadadehecho'], df_local['hogarescensados'])
    
    # Limpiamos infinitos y NaN finales
    df_local.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_local.fillna(0.0, inplace=True)

    return df_local


# Abrimos el csv como dataframe y calculamos métricas específicas de este script
ruta_csv = os.path.join(os.path.dirname(__file__), 'Datos', 'consolidado_limpio.csv')
df_raw = pd.read_csv(ruta_csv)
df = preparar_metricas(df_raw)

# Definimos X e Y usando las métricas calculadas de forma consistente
feature_cols = ['FEATURE_DORMITORIOS_PROM', 'FEATURE_TENENCIA_ARRIENDO', 'FEATURE_VIVIENDA_VULNERABLE', 'FEATURE_DENSIDAD_POBLACIONAL', 'FEATURE_VULNERABILIDAD_TENENCIA']

X = df[feature_cols].fillna(0.0)
y = df['TARGET_HOGARES_X_VIVIENDA'].fillna(0.0)
# Dividimos los datos
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamos el modelo de regresión lineal
model = LinearRegression()
model.fit(x_train, y_train)

# Predecir y evaluar

y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Imprimir resultados
print("Coeficientes:", model.coef_)
print("Intercepto:", model.intercept_)
print("MSE:", mse)
print("R2:", r2)

# Estos datos representan que:
print("\nInterpretación de los coeficientes:")
for nombre, coef in zip(feature_cols, model.coef_):
    print(f"- Por cada unidad que aumenta {nombre}, el TARGET_HOGARES_X_VIVIENDA cambia en {coef:.4f} unidades, manteniendo las otras variables constantes.")

# Graficar resultados de regresión lineal
graficar_regresion_lineal(df, 'TARGET_HOGARES_X_VIVIENDA', 'FEATURE_DORMITORIOS_PROM')
# Calcular residuos
residuos = y_test - y_pred

plt.figure(figsize=(8,5))
plt.scatter(y_pred, residuos, alpha=0.7)
plt.axhline(y=0)
plt.title("Gráfico de Residuos")
plt.xlabel("Valores Predichos")
plt.ylabel("Residuos (Error)")
plt.tight_layout()
plt.show()