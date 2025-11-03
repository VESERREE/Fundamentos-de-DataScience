import os
from Graficos import graficar_modelo_knn
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Limpieza import _safe_division, _to_numeric
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def preparar_metricas(df: pd.DataFrame) -> pd.DataFrame:
    # Genera métricas agregadas necesarias para el modelo de hacinamiento.
    df_local = df.copy()

    # Normalizamos las columnas base
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
    # Si faltan columnas, lanzamos un error
    if faltantes:
        # Lanzamos un error si faltan columnas
        raise KeyError(f'Faltan columnas necesarias en el DataFrame: {faltantes}')

    # Convertimos las columnas a numéricas
    for columna in columnas_base + columnas_dorm:
        # Convertimos a numérico y llenamos NaN con 0.0
        df_local[columna] = _to_numeric(df_local[columna]).fillna(0.0)

    # Cálculo de métricas agregadas
    viviendas_ocupadas = df_local['viviendasparticularesocupadasconmoradorespresentes']

    # Cálculo del total de hogares
    total_hogares = (
        df_local['viviendascon1hogar']
        + df_local['viviendascon2hogares'] * 2
        + df_local['viviendascon3hogares'] * 3
        + df_local['viviendascon4omashogares'] * 4
    )
    # Cálculo de la métrica objetivo: hogares por vivienda ocupada
    df_local['TARGET_HOGARES_X_VIVIENDA'] = _safe_division(total_hogares, viviendas_ocupadas)

    # Cálculo de la métrica: promedio de dormitorios por vivienda ocupada
    pesos_dorm = [0, 1, 2, 3, 4, 5, 6]
    # Calculamos el total de dormitorios ponderado
    total_dormitorios = pd.Series(0.0, index=df_local.index)
    # Calculamos el total de dormitorios ponderado
    for col, peso in zip(columnas_dorm, pesos_dorm):
        # Multiplicamos la columna de dormitorios por su peso
        total_dormitorios = total_dormitorios.add(df_local[col] * peso, fill_value=0.0)
    # Asignamos la métrica al DataFrame
    df_local['FEATURE_DORMITORIOS_PROM'] = _safe_division(total_dormitorios, viviendas_ocupadas)

    # Cálculo de la métrica: tenencia de vivienda en arriendo
    total_arriendo = df_local['arrendadaconcontrato'] + df_local['arrendadasincontrato']
    # Asignamos la métrica al DataFrame
    df_local['FEATURE_TENENCIA_ARRIENDO'] = _safe_division(total_arriendo, viviendas_ocupadas)

    # Cálculo de la métrica: viviendas vulnerables
    vulnerables = df_local['mediaguamejoraviviendadeemergenciaranchoochoza']
    # Asignamos la métrica al DataFrame
    df_local['FEATURE_VIVIENDA_VULNERABLE'] = _safe_division(vulnerables, viviendas_ocupadas)

    # Cálculo de métricas adicionales
    df_local['FEATURE_DENSIDAD_POBLACIONAL'] = _safe_division(
        # Población censada por viviendas ocupadas
        df_local['poblacioncensada'], viviendas_ocupadas
    )
    # Cálculo de la métrica: vulnerabilidad por tenencia
    df_local['FEATURE_VULNERABILIDAD_TENENCIA'] = _safe_division(
        # Ocupados de hecho por hogares censados
        df_local['ocupadadehecho'], df_local['hogarescensados']
    )

    # Limpiamos valores infinitos y NaN resultantes de las divisiones
    df_local.replace([np.inf, -np.inf], np.nan, inplace=True)
    # Rellenamos NaN con 0.0
    df_local.fillna(0.0, inplace=True)

    return df_local

# Esta funcion crea la columna binaria de riesgo basándose en un percentil del hacinamiento.
def generar_target(df: pd.DataFrame, percentil: float = 0.75) -> Tuple[pd.DataFrame, float]:
    # Crea columna binaria de riesgo basándose en un percentil del hacinamiento.
    umbral = df['TARGET_HOGARES_X_VIVIENDA'].quantile(percentil)
    # Crear la columna binaria de riesgo
    # Usamos el umbral para definir alto riesgo de hacinamiento
    df['TARGET_RIESGO_HACINAMIENTO'] = (df['TARGET_HOGARES_X_VIVIENDA'] >= umbral).astype(int)
    # Retornamos el DataFrame modificado y el umbral
    return df, float(umbral)

# Esta funcion ajusta el umbral de decisión para alcanzar un recall objetivo
def ajustar_umbral(probas: np.ndarray, y_true: np.ndarray, objetivo_recall: float = 0.75) -> float:
    # Busca un umbral de decisión que alcance, si es posible, el recall objetivo.
    mejor_thr = 0.5
    # Inicializamos las métricas de rendimiento
    mejor_recall = -1.0
    # Inicializamos la métrica F1
    mejor_f1 = -1.0

    # Recorremos posibles umbrales
    for thr in np.linspace(0.2, 0.8, 25):
        # Calculamos las predicciones binarias
        preds = (probas >= thr).astype(int)
        # Calculamos recall y precision
        recall = recall_score(y_true, preds, zero_division=0)
        # Calculamos la métrica F1
        precision = precision_score(y_true, preds, zero_division=0)
        # Evaluamos si cumple con el objetivo de recall
        if recall >= objetivo_recall and precision + recall > 0:
            # Calculamos la métrica F1
            f1 = 2 * precision * recall / (precision + recall)
            # Actualizamos si es mejor
            if f1 > mejor_f1:
                mejor_f1 = f1
                mejor_recall = recall
                mejor_thr = thr
        # Si no se alcanza el objetivo, buscamos el mejor recall posible
        elif mejor_recall < 0 and recall > mejor_recall:
            mejor_recall = recall
            mejor_thr = thr

    return mejor_thr


def main():
    ruta_csv = os.path.join(os.path.dirname(__file__), 'Datos', 'consolidado_limpio.csv')
    df_raw = pd.read_csv(ruta_csv)

    # Filtramos solo comunas de la Región Metropolitana de Santiago
    mask_region = None
    if 'codigoregion' in df_raw.columns:
        codigo_numeric = pd.to_numeric(df_raw['codigoregion'], errors='coerce')
        mask_region = codigo_numeric == 13
    if (mask_region is None or mask_region.sum() == 0) and 'region' in df_raw.columns:
        mask_region = df_raw['region'].astype(str).str.contains('santiago', case=False, na=False)
    if mask_region is None or mask_region.sum() == 0:
        raise ValueError('No se pudieron identificar comunas de la Región Metropolitana de Santiago en el dataset.')

    # Aplicamos el filtro
    df_raw = df_raw[mask_region]
    # Verificamos que hay comunas disponibles
    total_comunas = len(df_raw)
    # Si no hay comunas, lanzamos un error
    print(f'Comunas Región Metropolitana consideradas: {total_comunas}')
    # Preparamos las métricas necesarias
    df_metricas = preparar_metricas(df_raw)
    # Generamos la columna objetivo
    df_metricas, umbral = generar_target(df_metricas, percentil=0.75)

    feature_cols = [
        'FEATURE_DORMITORIOS_PROM',
        'FEATURE_TENENCIA_ARRIENDO',
        'FEATURE_VIVIENDA_VULNERABLE',
        'FEATURE_DENSIDAD_POBLACIONAL',
        'FEATURE_VULNERABILIDAD_TENENCIA',
    ]

    X = df_metricas[feature_cols].to_numpy()
    y = df_metricas['TARGET_RIESGO_HACINAMIENTO'].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Entrenamos el modelo de clasificación
    modelo = Pipeline(
        [
            # Usamos escalado estándar ya que las características pueden tener diferentes rangos
            ('scaler', StandardScaler()),
            # Clasificador logístico con balanceo de clases, max 500 iteraciones para convergencia
            ('clf', LogisticRegression(max_iter=500, class_weight='balanced')),
        ]
    )
    # Entrenamos el modelo
    modelo.fit(X_train, y_train)

    # Ajustamos el umbral para alcanzar el recall objetivo
    # Esto significa que buscamos un umbral que permita identificar al menos el 75% de las comunas en riesgo
    prob_test = modelo.predict_proba(X_test)[:, 1]
    # Ajustamos el umbral para alcanzar un recall objetivo del 75%
    umbral_optimo = ajustar_umbral(prob_test, y_test, objetivo_recall=0.75)
    # Aplicamos el umbral óptimo a las predicciones del set completo y del set de prueba
    y_pred_completo = (modelo.predict_proba(X)[:, 1] >= umbral_optimo).astype(int)
    y_pred_test = (prob_test >= umbral_optimo).astype(int)

    # Calculamos métricas de evaluación
    precision = precision_score(y, y_pred_completo, zero_division=0)
    # recall_score para calcular recall con las variables segun la definición
    recall = recall_score(y, y_pred_completo, zero_division=0)
    # Añadimos ROC-AUC que es útil para clasificación binaria ya que mide la capacidad de discriminación
    roc_auc = roc_auc_score(y, modelo.predict_proba(X)[:, 1])
    # Calculamos la matriz de confusión y el reporte de clasificación
    cm_total = confusion_matrix(y, y_pred_completo)
    # Generamos el reporte de clasificación
    reporte_total = classification_report(y, y_pred_completo, zero_division=0)

    print('=== Riesgo de Hacinamiento: Todas las comunas RM ===')
    print(f'Percentil usado para alto riesgo: {umbral:.3f}')
    print(f'Umbral óptimo aplicado: {umbral_optimo:.2f}')
    print('Confusion Matrix total:')
    print(cm_total)
    print('Metricas globales:')
    print(f'Precision: {precision:.3f}')
    print(f'Recall: {recall:.3f}')
    print(f'ROC-AUC: {roc_auc:.3f}')
    print('Classification Report (para todas las comunas):')
    print(reporte_total)
    # Graficamos los resultados del modelo KNN
    graficar_modelo_knn(
    y_test,
    y_pred_test,
    y_prob=prob_test,
    titulo="Modelo Logístico: Riesgo de Hacinamiento"
)


if __name__ == '__main__':
    main()