import requests
import pandas as pd

# 1. Definir la URL de la API
url = 'https://mindicador.cl/api/uf'

# 2. Hacer la petición GET a la API
response = requests.get(url)

# 3. Convertir la respuesta JSON a un diccionario de Python
data = response.json()

# 4. Convertir los datos a un DataFrame de Pandas
df_uf = pd.DataFrame(data['serie'])

# 5. ¡Analizar!
print(df_uf.head())