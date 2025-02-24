import requests
import json

# URL del endpoint de predicción
url = 'http://127.0.0.1:8000/predict/'

# Datos de ejemplo para la solicitud
data = {
    "opcion": "analizar",
    "data": []  # Puedes dejar esto vacío para la opción de análisis
}

try:
    # Enviar la solicitud POST al servidor
    response = requests.post(url, json=data)
    response.raise_for_status()  # Verificar si hay errores en la solicitud

    # Imprimir la respuesta en texto
    print("Texto de la respuesta del servidor:", response.text)

    # Intentar decodificar la respuesta a JSON solo si es posible
    try:
        response_json = response.json()
        # Guardar la respuesta en un archivo
        with open('respuesta.json', 'w') as file:
            json.dump(response_json, file, indent=4)
        print("La respuesta ha sido guardada en 'respuesta.json'")
    except json.decoder.JSONDecodeError:
        print("La respuesta del servidor no es un JSON válido.")
except requests.ConnectionError:
    print("No se pudo establecer una conexión con el servidor.")
except requests.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
