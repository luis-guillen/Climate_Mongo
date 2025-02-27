import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

def get_historical_data(ciudad):
    # Conectar a la base de datos MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CLimate-MongoDB"]
    collection = db["datos_climaticos_históricos"]

    # Obtener los datos climáticos de la ciudad especificada de la base de datos
    data = list(collection.find({"nombre": ciudad}))

    if not data:
        raise ValueError(f"No se encontraron datos para la ciudad: {ciudad}")

    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(data)

    # Verificar si la columna 'fecha' está presente
    if 'fecha' not in df.columns:
        raise KeyError("'fecha' no está en los datos obtenidos de MongoDB")

    # Convertir la columna 'fecha' a formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Verificar y convertir las temperaturas a tipo float
    if 'tmax' in df.columns:
        df['tmax'] = df['tmax'].str.replace(',', '.').astype(float)
    else:
        raise KeyError("'tmax' no está en los datos obtenidos de MongoDB")

    if 'tmin' in df.columns:
        df['tmin'] = df['tmin'].str.replace(',', '.').astype(float)
    else:
        raise KeyError("'tmin' no está en los datos obtenidos de MongoDB")

    # Calcular temperatura media
    df['tmed'] = (df['tmax'] + df['tmin']) / 2

    # Eliminar filas con NaN en 'tmed'
    df.dropna(subset=['tmed'], inplace=True)

    return df

def train_model(df):
    # Usar el día del año como característica
    df['day_of_year'] = df['fecha'].dt.dayofyear

    # Preparar los datos para el modelo
    X = df[['day_of_year']].values
    y = df['tmed'].values

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo HistGradientBoostingRegressor
    model = HistGradientBoostingRegressor()
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE: {mse}")

    return model

def predict_future_weather(model, num_days=7):
    # Obtener la fecha de hoy
    today = datetime.now()
    # Generar las fechas para los próximos días, comenzando desde mañana
    future_dates = [today + timedelta(days=i) for i in range(1, num_days + 1)]

    # Convertir las fechas futuras a 'day_of_year' para el modelo
    next_days = np.array([date.timetuple().tm_yday for date in future_dates]).reshape(-1, 1)

    # Predecir las temperaturas para los próximos días
    predicted_temperatures = model.predict(next_days)

    forecast = []
    for i, temp in enumerate(predicted_temperatures):
        forecast.append({
            "date": future_dates[i].strftime("%Y-%m-%d"),
            "temp_avg": round(temp, 1),
            "weather": "Clear"  # Simplificado; podrías añadir lógica para determinar el tipo de clima
        })

    return forecast



def get_city_forecast(ciudad):
    df = get_historical_data(ciudad)
    model = train_model(df)
    forecast = predict_future_weather(model)
    return forecast
