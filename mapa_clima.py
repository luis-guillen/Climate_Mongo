import os
from tkinter import messagebox

import folium
import json
import branca
import pymongo
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de MongoDB desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")


def seleccionar_imagen(clima):
    clima_dic = {
        'Clear': '/imagenes/sol.png',
        'Clouds': 'imagenes/nube.png',
        'Rain': '/imagenes/nube_lluvia.png',
        'Drizzle': '/imagenes/nube_lluvia.png',
        'Shower': 'imagenes/nube_lluvia.png',
        'Snow': '/imagenes/nieve.png',
        'Thunderstorm': '/imagenes/tormenta.png',
        'Mist': '/imagenes/sol.png',
        'Fog': '/imagenes/sol.png',
        'Wind': '/imagenes/sol.png',
        'Breeze': '/imagenes/sol.png'
    }
    return clima_dic.get(clima, '/imagenes/sol.png')


def precargar_datos():
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Climate-MongoDB"]
    collection = db["datos_climaticos_espana"]

    datos = {ciudad["name"]: ciudad for ciudad in collection.find()}
    return datos


def agregar_marcador(mapa, ciudad, datos):
    temperatura = datos["main"]["temp"]
    clima = datos["weather"][0]["main"]
    humedad = datos["main"]["humidity"]
    viento = datos["wind"]["speed"]
    icono = seleccionar_imagen(clima)

    # Crear contenido HTML estructurado
    html_content = f"""
    <div style="font-family: Arial, sans-serif; font-size: 12px;">
        <b>{ciudad}</b><br>
        Temperatura: {temperatura}°C<br>
        Clima: {clima}<br>
        Humedad: {humedad}%<br>
        Viento: {viento} m/s
    </div>
    """

    iframe = branca.element.IFrame(html=html_content, width=200, height=100)
    popup = folium.Popup(iframe, max_width=200)
    tooltip = f"{ciudad}: {temperatura}°C"

    folium.Marker(
        [datos["coord"]["lat"], datos["coord"]["lon"]],
        popup=popup,
        tooltip=tooltip,
        icon=folium.CustomIcon(icono, icon_size=(30, 30))
    ).add_to(mapa)


def generar_mapa_espana(provincias, datos_climaticos):
    mapa = folium.Map(location=[40.416775, -3.703790], zoom_start=6, tiles='CartoDB.Positron')
    for provincia in provincias["provincias"]:
        capital = provincia["capital"]
        datos = datos_climaticos.get(capital)
        if datos:
            agregar_marcador(mapa, capital, datos)
    mapa_html_path = "espana_mapa.html"
    mapa.save(mapa_html_path)
    return mapa_html_path

def generar_mapa_provincia(provincia, datos_climaticos):
    capital = provincia["capital"]
    datos_capital = datos_climaticos.get(capital)
    if datos_capital:
        mapa = folium.Map(location=[datos_capital["coord"]["lat"], datos_capital["coord"]["lon"]], zoom_start=10,
                          tiles='CartoDB.Positron')
        for ciudad in provincia["ciudades"]:
            datos_ciudad = datos_climaticos.get(ciudad)
            if datos_ciudad:
                agregar_marcador(mapa, ciudad, datos_ciudad)

        mapa_html_path = f"{provincia['nombre']}_mapa.html"
        mapa.save(mapa_html_path)
        return mapa_html_path
    else:
        messagebox.showerror("Error",
                             f"No se encontraron datos climáticos para la capital {capital} de {provincia['nombre']}")
        return None


def mostrar_mapa_clima(capital):
    with open('provincias.json', 'r', encoding='utf-8') as f:
        provincias = json.load(f)

    datos_climaticos = precargar_datos()

    provincia = next((prov for prov in provincias["provincias"] if prov["capital"].lower() == capital.lower()), None)
    if provincia:
        mapa_provincia_path = generar_mapa_provincia(provincia, datos_climaticos)
        if mapa_provincia_path:
            print(f"Mapa de la provincia {provincia['nombre']} generado: {mapa_provincia_path}")
            return mapa_provincia_path
        else:
            print(f"No hay datos climáticos para la provincia {provincia['nombre']}")
            return None
    else:
        print(f"No se encontró la provincia con la capital {capital}")
        return None


def mostrar_mapa_espana():
    with open('provincias.json', 'r', encoding='utf-8') as f:
        provincias = json.load(f)

    datos_climaticos = precargar_datos()

    mapa_path = generar_mapa_espana(provincias, datos_climaticos)
    print(f"Mapa de España generado en: {mapa_path}")  # Añade esta línea para depuración

    return mapa_path

