import json


def cargar_nombres_ciudades_espana(file_path):
    cities_spain_names = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for city in data:
                if city["country"] == "ES":
                    cities_spain_names.append(city["name"])
    except Exception as e:
        print(f"Error al cargar nombres de ciudades: {e}")

    return cities_spain_names


if __name__ == "__main__":
    file_path = "city_list_sin_duplicados.json"
    cities_spain_names = cargar_nombres_ciudades_espana(file_path)
    print(f"Ciudades de España: {len(cities_spain_names)}")
