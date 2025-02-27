import pymongo

def conectar_mongodb(uri, db_name):
    client = pymongo.MongoClient(uri)
    return client[db_name]

def almacenar_datos_ciudad(collection, datos_ciudad):
    try:
        collection.update_one(
            {"name": datos_ciudad["name"]},
            {"$set": datos_ciudad},
            upsert=True
        )
    except Exception as e:
        print(f"Error al almacenar datos en MongoDB: {e}")
