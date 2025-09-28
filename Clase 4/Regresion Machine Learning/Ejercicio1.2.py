import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 1. Datos y DataFrame
datos = {'Bajas': [25, 15, 35, 10, 40, 5, 30, 20],
         'Vehiculos_Destruidos': [2, 0, 3, 1, 5, 0, 4, 1],
         'Banderas_Capturadas': [5, 2, 8, 1, 10, 3, 7, 4],
         'SPM': [750, 400, 950, 300, 1200, 250, 1000, 550]}

df = pd.DataFrame(datos)

# 2. Definir X e Y
X = df[['Bajas', 'Vehiculos_Destruidos', 'Banderas_Capturadas']]
Y = df['SPM']

# 3. Dividir datos
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
# print(X_train, X_test, Y_train, Y_test)

# 4. Entrena modelo
model = LinearRegression()
model.fit(x_train, y_train)

# 5. Predecir y Evaluar
y_pred = model.predict(x_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Resultados de la Evaluacion: ")
print(f"RMSE:{rmse:.2f}")
print(f"R-cuadrado: {r2:.2f}")