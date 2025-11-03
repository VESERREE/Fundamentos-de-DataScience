import os
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from Graficos import graficar_arbol_decision
import numpy as np
import pandas as pd
from Limpieza import _safe_division, _to_numeric
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
TIPO_VIVIENDA_COLUMNAS: Dict[str, str] = {
    # Mapeo de columnas a nombres legibles
	'casaconaccesodirectodesdelacalle': 'Casa Calle',
	'casaencondominiocerrado': 'Casa Condominio',
	'departamentoenedificioconascensor': 'Depto Ascensor',
	'departamentoenedificiosinascensor': 'Depto Sin Ascensor',
	'viviendatradicionalindigenarukauotras': 'Vivienda Tradicional',
	'piezaencasaantiguaoconventillo': 'Pieza Interior',
	'mediaguamejoraviviendadeemergenciaranchoochoza': 'Mediagua/Emergencia',
	'movilcarpacasarodanteosimilar': 'Móvil/Carpa',
	'otrotipodeviviendaparticular': 'Otro Particular',
}


def preparar_metricas(df: pd.DataFrame) -> pd.DataFrame:
    # Creamos una copia para no modificar el original
	df_local = df.copy()

	# Definimos las columnas necesarias para el modelo
	columnas_necesarias: List[str] = [
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
		'cedidaportrabajooservicio',
		'cedidaporfamiliaruotro',
		'usufructosolousoygoce',
		'propiedadensucesionylitigio',
		'tenenciadelaviviendanodeclarada',
		'viviendascensadas',
	] + list(TIPO_VIVIENDA_COLUMNAS.keys())

	columnas_dorm = [
     # Definimos las columnas de dormitorios
		'0dormitorios',
		'1dormitorio',
		'2dormitorios',
		'3dormitorios',
		'4dormitorios',
		'5dormitorios',
		'6omasdormitorios',
	]

	faltantes = [col for col in columnas_necesarias + columnas_dorm if col not in df_local.columns]
	# Verificamos si faltan columnas
	if faltantes:
		raise KeyError(f'Faltan columnas necesarias: {faltantes}')

	# Convertimos a numérico y llenamos NaNs con 0.0
	for columna in columnas_necesarias + columnas_dorm:
		# Convertimos a numérico y llenamos NaNs con 0.0
		df_local[columna] = _to_numeric(df_local[columna]).fillna(0.0)

	viviendas_ocupadas = df_local['viviendasparticularesocupadasconmoradorespresentes']

	# Calculamos el total de hogares
	# Multiplicando por el número de hogares correspondiente
	total_hogares = (
		df_local['viviendascon1hogar']
		+ df_local['viviendascon2hogares'] * 2
		+ df_local['viviendascon3hogares'] * 3
		+ df_local['viviendascon4omashogares'] * 4
	)
 	# Definimos la variable objetivo
	df_local['FEATURE_PROM_HOGARES'] = _safe_division(total_hogares, viviendas_ocupadas)

	pesos_dorm = [0, 1, 2, 3, 4, 5, 6]
	# Calculamos el promedio de dormitorios
	total_dormitorios = pd.Series(0.0, index=df_local.index)
	# Calculamos el promedio de dormitorios
	for col, peso in zip(columnas_dorm, pesos_dorm):
		# Sumamos el total ponderado de dormitorios
		total_dormitorios = total_dormitorios.add(df_local[col] * peso, fill_value=0.0)
	# Asignamos la métrica calculada
	df_local['FEATURE_DORMITORIOS_PROM'] = _safe_division(total_dormitorios, viviendas_ocupadas)

	# Calculamos la tenencia en arriendo
	total_arriendo = df_local['arrendadaconcontrato'] + df_local['arrendadasincontrato']
	# Asignamos la métrica calculada
	df_local['FEATURE_TENENCIA_ARRIENDO'] = _safe_division(total_arriendo, viviendas_ocupadas)

	# Asignamos la métrica calculada
	df_local['FEATURE_VIVIENDA_VULNERABLE'] = _safe_division(
		# Viviendas en situación de vulnerabilidad
		df_local['mediaguamejoraviviendadeemergenciaranchoochoza'], viviendas_ocupadas
	)

	# Calculamos otras métricas
	df_local['FEATURE_DENSIDAD_POBLACIONAL'] = _safe_division(
		# Población censada por vivienda ocupada
		df_local['poblacioncensada'], viviendas_ocupadas
	)
 	# Asignamos la métrica calculada
	df_local['FEATURE_VULNERABILIDAD_TENENCIA'] = _safe_division(
		# Hogares ocupados de hecho sobre hogares censados
		df_local['ocupadadehecho'], df_local['hogarescensados']
	)

	# Otras métricas de tenencia
	df_local['FEATURE_TENENCIA_PROPIA'] = _safe_division(df_local['propiapagada'], df_local['hogarescensados'])
	# Asignamos la métrica calculada
	df_local['FEATURE_TENENCIA_PROPIA_DEUDA'] = _safe_division(
		# Hogares con deuda sobre hogares censados
		df_local['propiapagandose'], df_local['hogarescensados']
	)
	# Asignamos la métrica calculada
	df_local['FEATURE_TENENCIA_CEDIDA'] = _safe_division(
		# Hogares con tenencia cedida sobre hogares censados
		df_local['cedidaporfamiliaruotro'] + df_local['cedidaportrabajooservicio'],
		# Hogares censados
		df_local['hogarescensados'],
	)
	# Asignamos la métrica calculada
	df_local['FEATURE_TENENCIA_USUFRUCTO'] = _safe_division(
		# Hogares en usufructo sobre hogares censados
		df_local['usufructosolousoygoce'], df_local['hogarescensados']
	)

	# Reemplazamos infinitos y NaNs
	df_local.replace([np.inf, -np.inf], np.nan, inplace=True)
	# Llenamos NaNs con 0.0
	df_local.fillna(0.0, inplace=True)

	return df_local

#	 Definimos la función para generar el target de tipología
def generar_target_tipologia(df: pd.DataFrame) -> Tuple[pd.Series, List[str]]:
    # Definimos las columnas relevantes
	columns = list(TIPO_VIVIENDA_COLUMNAS.keys())
  	# Creamos un sub-DataFrame con las columnas relevantes
	sub_df = df[columns]
	# Obtenemos el índice de la columna con el valor máximo para cada fila
	idx_max = sub_df.values.argmax(axis=1)
	# Generamos las etiquetas correspondientes para cada fila 
	labels = [TIPO_VIVIENDA_COLUMNAS[columns[i]] for i in idx_max]
	# Devolvemos las etiquetas generadas y las columnas utilizadas
	return pd.Series(labels, index=df.index, name='TIPO_VIVIENDA_PREDOMINANTE'), columns


def main() -> None:
	# Cargamos el dataset
	ruta_csv = os.path.join(os.path.dirname(__file__), 'Datos', 'consolidado_limpio.csv')
	# Leemos el archivo CSV
	df_raw = pd.read_csv(ruta_csv)
	# Creamos una máscara (booleano) para filtrar por Región Metropolitana
	mask_region = None
	# Filtramos por Región Metropolitana
	# Verificamos si existe la columna 'codigoregion'
	if 'codigoregion' in df_raw.columns:
		# Convertimos a numérico y creamos la máscara
		codigo_numeric = pd.to_numeric(df_raw['codigoregion'], errors='coerce')
		# Creamos la máscara para la Región Metropolitana
		mask_region = codigo_numeric == 13
		# Si no se encontró, intentamos con la columna 'region'
	if (mask_region is None or mask_region.sum() == 0) and 'region' in df_raw.columns:
		# Creamos la máscara buscando 'santiago' en la columna 'region'
		mask_region = df_raw['region'].astype(str).str.contains('santiago', case=False, na=False)
	# Si aún no se encontró, lanzamos un error
	if mask_region is None or mask_region.sum() == 0:
		# Lanzamos un error si no se pudo identificar la Región Metropolitana
		raise ValueError('No se pudieron identificar comunas de la Región Metropolitana en el dataset.')

	df_raw = df_raw[mask_region]
	# Contamos las comunas consideradas
	total_comunas = len(df_raw)
	# Imprimimos el total de comunas consideradas
	print(f'Comunas Región Metropolitana consideradas: {total_comunas}')

	# Definimos las columnas de análisis
	analisis_columns = [
		'casaconaccesodirectodesdelacalle',
		'departamentoenedificioconascensor',
		'departamentoenedificiosinascensor',
		'casaencondominiocerrado',
	]
	# Convertimos las columnas a numéricas
	df_numeric = df_raw.copy()
	# Recorremos y convertimos
	for col in analisis_columns:
		# Convertimos a numérico
		if col in df_numeric.columns:
			# Convertimos a numérico
			df_numeric[col] = _to_numeric(df_numeric[col])

	df_metricas = preparar_metricas(df_raw)
	# Generamos el target de tipología
	target_series, columnas_tipologia = generar_target_tipologia(df_metricas)
	# Contamos las clases totales
	conteo_clases_total = target_series.value_counts().sort_index()
	# Imprimimos la distribución total por tipología
	print('Distribución total por tipología:')
	# Recorremos e imprimimos
	for clase, cantidad in conteo_clases_total.items():
		# Imprimimos la clase y su cantidad
		print(f'  {clase}: {cantidad}')

	df_metricas = df_metricas.assign(TIPO_VIVIENDA_PREDOMINANTE=target_series)

	# Definimos las columnas de características
	feature_cols = [
		'FEATURE_PROM_HOGARES',
		'FEATURE_DORMITORIOS_PROM',
		'FEATURE_TENENCIA_ARRIENDO',
		'FEATURE_VIVIENDA_VULNERABLE',
		'FEATURE_DENSIDAD_POBLACIONAL',
		'FEATURE_VULNERABILIDAD_TENENCIA',
		'FEATURE_TENENCIA_PROPIA',
		'FEATURE_TENENCIA_PROPIA_DEUDA',
		'FEATURE_TENENCIA_CEDIDA',
		'FEATURE_TENENCIA_USUFRUCTO',
	]

	# Filtramos el DataFrame para eliminar filas con NaNs en las columnas de interés
	df_modelo = df_metricas.dropna(subset=feature_cols + ['TIPO_VIVIENDA_PREDOMINANTE'])

	# Contamos las clases presentes
	conteo_clases = df_modelo['TIPO_VIVIENDA_PREDOMINANTE'].value_counts()
	# Filtramos las clases con al menos dos observaciones
	clases_validas = conteo_clases[conteo_clases >= 2].index
	# Filtramos el DataFrame para mantener solo las clases válidas
	df_modelo = df_modelo[df_modelo['TIPO_VIVIENDA_PREDOMINANTE'].isin(clases_validas)]
	# Verificamos que haya al menos dos clases válidas
	if len(clases_validas) < 2:
		# Lanzamos un error si no hay suficientes clases válidas
		raise ValueError('No hay suficientes clases con al menos dos observaciones para entrenar el modelo.')

	# Preparamos los datos para el modelo
	X = df_modelo[feature_cols].to_numpy()
	# Definimos el target
	y = df_modelo['TIPO_VIVIENDA_PREDOMINANTE'].astype(str).to_numpy()

	# Codificamos las etiquetas de clase
	encoder = LabelEncoder()
	# Ajustamos y transformamos las etiquetas
	y_encoded = encoder.fit_transform(y)

	# Configuramos la validación cruzada estratificada usando StratifiedKFold que hace splits manteniendo la proporción de clases
	# shuffle=True para aleatorizar y random_state=42 para que sea reproducible
	kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

	# Entrenamos y evaluamos el Árbol de Decisión
	clf_tree = DecisionTreeClassifier(max_depth=6, random_state=42)
	# Realizamos predicciones con validación cruzada
	y_pred_tree = cross_val_predict(clf_tree, X, y_encoded, cv=kfold)
	# Calculamos la exactitud
	acc_tree = accuracy_score(y_encoded, y_pred_tree)

	clf_rf = RandomForestClassifier(
	# Configuramos el Random Forest
		n_estimators=300,
		max_depth=None,
		random_state=42,
		n_jobs=-1,
	)
	# Entrenamos y evaluamos el Random Forest
	y_pred_rf = cross_val_predict(clf_rf, X, y_encoded, cv=kfold, n_jobs=-1)
	# Calculamos la exactitud
	acc_rf = accuracy_score(y_encoded, y_pred_rf)

	print('=== Árbol de Decisión (validación cruzada, todas las comunas) ===')
	print(f'Exactitud: {acc_tree:.3f}')
	print('Reporte de clasificación:')
	print(classification_report(y_encoded, y_pred_tree, target_names=encoder.classes_, zero_division=0))

	print('\n=== Random Forest (validación cruzada, todas las comunas) ===')
	print(f'Exactitud: {acc_rf:.3f}')
	print('Reporte de clasificación:')
	print(classification_report(y_encoded, y_pred_rf, target_names=encoder.classes_, zero_division=0))

	# Entrenamos modelos finales con todo el set para obtener importancias.
	clf_tree.fit(X, y_encoded)
	clf_rf.fit(X, y_encoded)

	# Obtenemos las importancias de las características
	importancias_tree = clf_tree.feature_importances_
	importancias_rf = clf_rf.feature_importances_

	# Función para mostrar importancias
	def mostrar_importancias(nombre_modelo: str, importancias: np.ndarray) -> None:
		ranking = sorted(zip(feature_cols, importancias), key=lambda x: x[1], reverse=True)
		print(f'\nImportancia de variables ({nombre_modelo}):')
		for feature, score in ranking:
			print(f'  {feature}: {score:.3f}')

	mostrar_importancias('Árbol', importancias_tree)
	mostrar_importancias('Random Forest', importancias_rf)
	# Graficar resultados del Árbol de Decisión
	graficar_arbol_decision(clf_tree, feature_cols, encoder.classes_	)

if __name__ == '__main__':
    main()