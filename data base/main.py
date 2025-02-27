from load_city_names import cargar_nombres_ciudades_espana
from weather_api import obtener_datos_ciudad
from db_operations import conectar_mongodb, almacenar_datos_ciudad


def main():
    # Configuración
    file_path = "city_list_sin_duplicados.json"
    mongo_uri = "mongodb://localhost:27017/"
    db_name = "Climate-MongoDB"
    collection_name = "datos_climaticos_espana"

    # Cargar nombres de ciudades de España
    cities_spain_names = cargar_nombres_ciudades_espana(file_path)

    # Conectar a MongoDB
    db = conectar_mongodb(mongo_uri, db_name)
    collection = db[collection_name]

    # Obtener y almacenar datos climáticos
    for ciudad in cities_spain_names:
        datos_ciudad = obtener_datos_ciudad(ciudad)
        if datos_ciudad:
            almacenar_datos_ciudad(collection, datos_ciudad)

    print("Datos meteorológicos de todas las ciudades de España almacenados correctamente en MongoDB.")


if __name__ == "__main__":
    main()
