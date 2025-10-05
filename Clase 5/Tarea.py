'''
Una corredora de propiedades en Santiago quiere predecir el precio (en UF) de departamentos. 
Tienen los siguientes datos:
datos = {'Superficie_m2': [50, 70, 65, 90, 45], 
          'Num_Habitaciones': [1, 2, 2, 3, 1], 
          'Distancia_Metro_km': [0.5, 1.2, 0.8, 0.2, 2.0], 
          'Precio_UF': [2500, 3800, 3500, 5200, 2100]}
Construye un modelo de regresión lineal múltiple para predecir el 'Precio_UF' y 
evalúa su rendimiento.
'''
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

datos = {'Superficie_m2': [50, 70, 65, 90, 45], 
         'Num_Habitaciones': [1, 2, 2, 3, 1], 
         'Distancia_Metro_km': [0.5, 1.2, 0.8, 0.2, 2.0], 
         'Precio_UF': [2500, 3800, 3500, 5200, 2100]}

df = pd.DataFrame(datos)

# Definimos X e Y
X = df[['Superficie_m2', 'Num_Habitaciones', 'Distancia_Metro_km']]
Y= df['Precio_UF']

# Dividimos los datos
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Entrenamos el modelo
model = LinearRegression()
model.fit(x_train, y_train)

# Predecir y evaluar
y_pred = model.predict(x_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Imprimir los resultados
print(f'Resultados de la Evaluación')
print(f'RMSE = {rmse:.2f} (En promedio el valor de los departamentos en UF se desvia en {rmse:.2f} puntos)')
print(f'R-Cuadrado = {r2:.2f} (El {r2:.0%} de la variación en el valor de los departamentos en UF es explicado por los datos de: Superficie por metro cuadrado, cantidad de habitaciones y la distancia en metros')