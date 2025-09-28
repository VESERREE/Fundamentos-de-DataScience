import pandas as pd
import numpy as np
from sklearn.linear_model import PoissonRegressor

'''
Datos sacados de: https://www.goal.com/es-cl/
'''


datos = {
    # Datos históricos de partidos entre Universidad de Chile y La Serena
    'Equipo 1': ['Universidad de Chile'] * 14,
    'Equipo 2': ['La Serena'] * 14,
    'Goles Anotados Equipo 1': [0, 2, 5, 2, 1, 4, 0, 4, 1, 1, 0, 3, 0, 2],
    'Goles Anotados Equipo 2': [1, 1, 1, 4, 4, 5, 1, 0, 0, 3, 1, 0, 0, 2],
    'Localia Equipo 1': [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    'Localia Equipo 2': [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    'Posesion Equipo 1': [56.9, 55.8, 64.7, 59.3, 55.5, 70.0, 66.1, 53.2, 53.8, 31.5, 65.8, 57, 59.5, 50.3],
    'Posesion Equipo 2': [43.1, 44.2, 35.3, 40.7, 44.5, 30.0, 33.9, 46.8, 46.2, 68.5, 34.2, 39, 40.5, 49.7],
}
df = pd.DataFrame(datos)

# Features con lag
df['Promedio_Goles_Anotados_Equipo_1'] = df['Goles Anotados Equipo 1'].shift(1).rolling(5, min_periods=2).mean().fillna(0)
df['Promedio_Goles_Anotados_Equipo_2'] = df['Goles Anotados Equipo 2'].shift(1).rolling(5, min_periods=2).mean().fillna(0)
# Calculamos la diferencia de posesión para cada partido
df['Diferencia_Posesion'] = (df['Posesion Equipo 1'] - df['Posesion Equipo 2']).fillna(0)

features = ['Localia Equipo 1', 'Localia Equipo 2', 'Diferencia_Posesion', 'Promedio_Goles_Anotados_Equipo_1', 'Promedio_Goles_Anotados_Equipo_2']
X = df[features]
# Variable objetivo: goles anotados por cada equipo
y_t1 = df['Goles Anotados Equipo 1']
y_t2 = df['Goles Anotados Equipo 2']

# Entrenamiento
m1 = PoissonRegressor(alpha=1.0, max_iter=1000)
m2 = PoissonRegressor(alpha=1.0, max_iter=1000)
# Entrenamos un modelo para cada equipo
m1.fit(X, y_t1)
m2.fit(X, y_t2)

# Métricas de ajuste para ambos modelos
from sklearn.metrics import mean_squared_error, r2_score
y_pred_t1 = m1.predict(X)
y_pred_t2 = m2.predict(X)
rmse_t1 = np.sqrt(mean_squared_error(y_t1, y_pred_t1))
rmse_t2 = np.sqrt(mean_squared_error(y_t2, y_pred_t2))
r2_t1 = r2_score(y_t1, y_pred_t1)
r2_t2 = r2_score(y_t2, y_pred_t2)

# Resultados de evaluación Equipo 1
print("Resultados de la Evaluacion - Universidad de Chile:")
print(f'RMSE: {rmse_t1:.2f}')
print(f'Las predicciones en promedio se desvían en {rmse_t1:.2f} goles del resultado real')

print(f'\nR²: {r2_t1:.2f} ({r2_t1:.0%})')
print(f'El modelo explica el {r2_t1:.0%} de la variabilidad en los goles marcados')

# Resultados de evaluación Equipo 2
print("\nResultados de la Evaluacion - La Serena:")
print(f'RMSE: {rmse_t2:.2f}')
print(f'Las predicciones en promedio se desvían en {rmse_t2:.2f} goles del resultado real')

print(f'\nR²: {r2_t2:.2f} ({r2_t2:.0%})')
print(f'El modelo explica el {r2_t2:.0%} de la variabilidad en los goles marcados')

# Predicción del partido nuevo
Localia1 = int(round(df['Localia Equipo 1'].mean()))
Localia2 = int(round(df['Localia Equipo 2'].mean()))
Diferencia_Posesion = (df['Posesion Equipo 1'].mean() - df['Posesion Equipo 2'].mean())
Promedio_Goles_E1 = df['Promedio_Goles_Anotados_Equipo_1'].iloc[-1]
Promedio_Goles_E2 = df['Promedio_Goles_Anotados_Equipo_2'].iloc[-1]

# Creamos el DataFrame con los datos del partido a predecir
x_new = pd.DataFrame([{
    'Localia Equipo 1': Localia1,
    'Localia Equipo 2': Localia2,
    'Diferencia_Posesion': Diferencia_Posesion,
    'Promedio_Goles_Anotados_Equipo_1': Promedio_Goles_E1,
    'Promedio_Goles_Anotados_Equipo_2': Promedio_Goles_E2
}], columns=features)

# Predicción de goles esperados para cada equipo
Goles_esperados_E1 = float(m1.predict(x_new).clip(min=1e-6)[0])
Goles_esperados_E2 = float(m2.predict(x_new).clip(min=1e-6)[0])

print("\n=== Goles esperados ===")
print(f"U. de Chile: {Goles_esperados_E1:.2f}")
print(f"La Serena:   {Goles_esperados_E2:.2f}")

# Marcador más probable
# Simulamos muchos partidos para estimar el marcador más probable
rng = np.random.default_rng(42)  # Generador de números aleatorios reproducible
n_sim = 10000  # Número de simulaciones

# Goles simulados para cada equipo
sim_udechile = rng.poisson(Goles_esperados_E1, size=n_sim)
sim_laserena = rng.poisson(Goles_esperados_E2, size=n_sim)

# Calculamos el marcador más frecuente en las simulaciones
marcadores, conteos = np.unique(np.vstack([sim_udechile, sim_laserena]).T, axis=0, return_counts=True)
idx_moda = np.argmax(conteos)
marcador_mas_probable = tuple(marcadores[idx_moda])

print(f"\nMarcador más probable: U. de Chile {marcador_mas_probable[0]} - {marcador_mas_probable[1]} La Serena")