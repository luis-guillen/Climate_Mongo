import json


def eliminar_duplicados_ciudades(archivo_entrada, archivo_salida):
    nombres_unicos = set()
    ciudades_sin_duplicados = []

    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for ciudad in data:
                nombre_ciudad = ciudad['name']
                if nombre_ciudad not in nombres_unicos:
                    nombres_unicos.add(nombre_ciudad)
                    ciudades_sin_duplicados.append(ciudad)

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(ciudades_sin_duplicados, f, indent=4, ensure_ascii=False)

        print(f"Longitud de datos originales: {len(data)}")
        print(f"Longitud de datos sin duplicados: {len(ciudades_sin_duplicados)}")
    except Exception as e:
        print(f"Error al procesar los archivos JSON: {e}")


if __name__ == "__main__":
    eliminar_duplicados_ciudades('city.list.json', 'city_list_sin_duplicados.json')
