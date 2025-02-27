import os
import pymongo
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la URI de MongoDB
MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    client = pymongo.MongoClient(MONGO_URI)
    return client["GeoClima"]
