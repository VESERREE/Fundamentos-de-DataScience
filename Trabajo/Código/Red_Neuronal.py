import os
from typing import List
from Graficos import graficar_red_neuronal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Limpieza import _safe_division, _to_numeric
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def preparar_metricas(df: pd.DataFrame) -> pd.DataFrame:
	df_local = df.copy()
	# Definimos las columnas necesarias
	columnas_base: List[str] = [
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
		'propiapagada',
		'propiapagandose',
		'cedidaporfamiliaruotro',
		'cedidaportrabajooservicio',
		'usufructosolousoygoce',
		'propiedadensucesionylitigio',
		'tenenciadelaviviendanodeclarada',
		'viviendascensadas',
		'0_14',
		'15_64',
		'65anosomas',
		'indicedeenvejecimiento',
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
		raise KeyError(f'Faltan columnas necesarias: {faltantes}')

	# Convertimos a numérico y llenamos NaN con 0.0
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
	# Cálculo de métricas específicas
	df_local['FEATURE_PROM_HOGARES'] = _safe_division(total_hogares, viviendas_ocupadas)

	# Cálculo del promedio de dormitorios por vivienda ocupada
	pesos_dorm = [0, 1, 2, 3, 4, 5, 6]
	# Inicializamos la serie para el total de dormitorios
	total_dormitorios = pd.Series(0.0, index=df_local.index)
 	# Recorremos las columnas de dormitorios y sus pesos
	for col, peso in zip(columnas_dorm, pesos_dorm):
		# Multiplicamos la columna de dormitorios por su peso
		total_dormitorios = total_dormitorios.add(df_local[col] * peso, fill_value=0.0)
	# Asignamos la métrica calculada
	df_local['FEATURE_DORMITORIOS_PROM'] = _safe_division(total_dormitorios, viviendas_ocupadas)
	# Cálculo del total de viviendas en arriendo
	total_arriendo = df_local['arrendadaconcontrato'] + df_local['arrendadasincontrato']
	# Asignamos la métrica calculada
	df_local['FEATURE_TENENCIA_ARRIENDO'] = _safe_division(total_arriendo, viviendas_ocupadas)

	# Cálculo de métricas adicionales
	df_local['FEATURE_VIVIENDA_VULNERABLE'] = _safe_division(
		# Cálculo de viviendas vulnerables
		df_local['mediaguamejoraviviendadeemergenciaranchoochoza'], viviendas_ocupadas
	)
	# Cálculo de densidad poblacional
	df_local['FEATURE_DENSIDAD_POBLACIONAL'] = _safe_division(
		# Cálculo de densidad poblacional
		df_local['poblacioncensada'], viviendas_ocupadas
	)
	# Cálculo de métricas adicionales relacionadas con tenencia y propiedad
	df_local['FEATURE_VULNERABILIDAD_TENENCIA'] = _safe_division(
		df_local['ocupadadehecho'], df_local['hogarescensados']
	)

	# Feature de tenencia por tipo
	# Ya sea propia, deuda, cedida o usufructo
	df_local['FEATURE_TENENCIA_PROPIA'] = _safe_division(df_local['propiapagada'], df_local['hogarescensados'])
	df_local['FEATURE_TENENCIA_DEUDA'] = _safe_division(df_local['propiapagandose'], df_local['hogarescensados'])
	df_local['FEATURE_TENENCIA_CEDIDA'] = _safe_division(
		df_local['cedidaporfamiliaruotro'] + df_local['cedidaportrabajooservicio'],
		df_local['hogarescensados'],
	)
	# Feature de tenencia por usufructo
	df_local['FEATURE_TENENCIA_USUFRUCTO'] = _safe_division(
		df_local['usufructosolousoygoce'], df_local['hogarescensados']
	)

	# Feature de proporción de viviendas en sucesión o litigio
	df_local['FEATURE_PROP_SUCE_LITIGIO'] = _safe_division(
		df_local['propiedadensucesionylitigio'], df_local['hogarescensados']
	)

	# Feature de proporción de viviendas no declaradas
	df_local['FEATURE_PROP_NO_DECLARADA'] = _safe_division(
		df_local['tenenciadelaviviendanodeclarada'], df_local['hogarescensados']
	)

	grupo_total = df_local['0_14'] + df_local['15_64'] + df_local['65anosomas']
	grupo_ponderado = (
		df_local['0_14'] * 7.5
		+ df_local['15_64'] * 39.5
		+ df_local['65anosomas'] * 72.0
	)
	df_local['FEATURE_EDAD_PROM'] = _safe_division(grupo_ponderado, grupo_total)

	df_local.replace([np.inf, -np.inf], np.nan, inplace=True)
	df_local.fillna(0.0, inplace=True)

	return df_local


def main() -> None:
	ruta_csv = os.path.join(os.path.dirname(__file__), 'Datos', 'consolidado_limpio.csv')
	df_raw = pd.read_csv(ruta_csv)

	mask_region = None
	if 'codigoregion' in df_raw.columns:
		codigo_numeric = pd.to_numeric(df_raw['codigoregion'], errors='coerce')
		mask_region = codigo_numeric == 13
	if (mask_region is None or mask_region.sum() == 0) and 'region' in df_raw.columns:
		mask_region = df_raw['region'].astype(str).str.contains('santiago', case=False, na=False)
	if mask_region is None or mask_region.sum() == 0:
		raise ValueError('No se pudieron identificar comunas de la Región Metropolitana de Santiago en el dataset.')

	df_raw = df_raw[mask_region]
	print(f'Comunas Región Metropolitana consideradas: {mask_region.sum()}')

	anuncio_cols = [
		'comuna',
		'casaconaccesodirectodesdelacalle',
		'departamentoenedificioconascensor',
		'departamentoenedificiosinascensor',
	]
	sample_viviendas = df_raw[anuncio_cols].copy()
	for col in anuncio_cols[1:]:
		sample_viviendas[col] = _to_numeric(sample_viviendas[col])
	print('Ejemplo stock habitacional bruto (primeras comunas filtradas):')
	print(sample_viviendas.head())
	df_metricas = preparar_metricas(df_raw)

	feature_cols = [
		'FEATURE_PROM_HOGARES',
		'FEATURE_DORMITORIOS_PROM',
		'FEATURE_TENENCIA_ARRIENDO',
		'FEATURE_VIVIENDA_VULNERABLE',
		'FEATURE_DENSIDAD_POBLACIONAL',
		'FEATURE_VULNERABILIDAD_TENENCIA',
		'FEATURE_TENENCIA_PROPIA',
		'FEATURE_TENENCIA_DEUDA',
		'FEATURE_TENENCIA_CEDIDA',
		'FEATURE_TENENCIA_USUFRUCTO',
		'FEATURE_PROP_SUCE_LITIGIO',
		'FEATURE_PROP_NO_DECLARADA',
		'FEATURE_EDAD_PROM',
	]

	df_modelo = df_metricas.dropna(subset=feature_cols + ['indicedeenvejecimiento'])

	X = df_modelo[feature_cols].to_numpy()
	y = df_modelo['indicedeenvejecimiento'].to_numpy()

	X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=0.2,
		random_state=42,
	)

	modelo = Pipeline(
		[
			('scaler', StandardScaler()),
			(
				'mlp',
				MLPRegressor(
					hidden_layer_sizes=(64, 32),
					activation='relu',
					solver='adam',
					alpha=0.001,
					learning_rate_init=0.003,
					max_iter=2000,
					early_stopping=True,
					n_iter_no_change=20,
					validation_fraction=0.2,
					random_state=42,
				),
			),
		]
	)

	modelo.fit(X_train, y_train)

	y_pred = modelo.predict(X_test)

	mae = mean_absolute_error(y_test, y_pred)
	mse_value = mean_squared_error(y_test, y_pred)
	rmse = float(np.sqrt(mse_value))
	r2 = r2_score(y_test, y_pred)

	print('=== Red Neuronal MLP: Índice de Envejecimiento ===')
	print(f'MAE: {mae:.2f}')
	print(f'RMSE: {rmse:.2f}')
	print(f'R^2: {r2:.3f}')

	dif_abs = np.abs(y_test - y_pred)
	top_indices = np.argsort(dif_abs)[-5:]
	print('\nMayores diferencias (pred vs real):')
	for idx in top_indices:
		print(f'  Real: {y_test[idx]:.2f} | Predicho: {y_pred[idx]:.2f} | Error Absoluto: {dif_abs[idx]:.2f}')
	print('\nMenores diferencias (pred vs real):')
 
# Graficar resultados de la Red Neuronal
	graficar_red_neuronal(y_test, y_pred)
if __name__ == '__main__':
    main()