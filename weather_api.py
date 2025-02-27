import os
import requests
from tkinter import messagebox
from dotenv import load_dotenv
import pymongo

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las API keys desde las variables de entorno
OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")
OPEN_WEATHER_MAP_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'
MONGO_URI = os.getenv("MONGO_URI")
# Función para obtener el clima de la ubicación actual
def get_location_weather(lat, lon):
    try:
        weather_query_params = {
            'lat': lat,
            'lon': lon,
            'appid': OPEN_WEATHER_MAP_API_KEY,
            'units': 'metric'
        }

        response = requests.get(OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
        weather_data = response.json()

        if response.status_code == 401:
            raise ValueError("Clave API inválida para OpenWeatherMap.")

        try:
            temperature = weather_data['main']['temp']
            return temperature
        except KeyError:
            messagebox.showerror("Error", "No se pudo obtener los datos del clima.")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Función para obtener el clima de la ciudad ingresada por el usuario
def get_city_weather(city_name):
    weather_query_params = {
        'q': city_name,
        'appid': OPEN_WEATHER_MAP_API_KEY,
        'units': 'metric'
    }

    response = requests.get(OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
    weather_data = response.json()

    if response.status_code == 401:
        messagebox.showerror("Error", "Clave API inválida para OpenWeatherMap.")
        return None

    try:
        temperature = weather_data['main']['temp']
        return temperature
    except KeyError:
        messagebox.showerror("Error", "No se pudo obtener los datos del clima.")
        return None

# Función para obtener el nombre de la ubicación actual
def get_location_name(lat, lon):
    try:
        geo_query_params = {
            'lat': lat,
            'lon': lon,
            'appid': OPEN_WEATHER_MAP_API_KEY
        }

        response = requests.get("http://api.openweathermap.org/geo/1.0/reverse", params=geo_query_params)
        geo_data = response.json()

        if response.status_code == 401:
            raise ValueError("Clave API inválida para OpenWeatherMap.")

        try:
            location_name = geo_data[0]['name']
            return location_name
        except KeyError:
            messagebox.showerror("Error", "No se pudo obtener el nombre de la ubicación.")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def obtener_datos_ciudad(nombre_ciudad):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client["GeoClima"]
        collection = db["datos_climaticos_espana"]

        # Realizar la consulta a la base de datos
        datos_ciudad = collection.find_one({"name": nombre_ciudad})
        if datos_ciudad is None:
            raise ValueError(f"No se encontraron datos para la ciudad: {nombre_ciudad}")

        return datos_ciudad
    except pymongo.errors.ConnectionError as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

