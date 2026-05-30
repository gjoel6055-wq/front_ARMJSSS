import requests
from constants import API_BASE_URL

def registrar_nota_api(datos_nota):
    url = f"{API_BASE_URL}/notas"
    try:
        respuesta = requests.post(url, json=datos_nota)
        if respuesta.status_code == 201:
            return {"exito": True, "datos": respuesta.json()}
        else:
            return {"exito": False, "error": "Error al procesar el registro de la nota."}
    except requests.exceptions.RequestException:
        return {"exito": False, "error": "Error de conexión con la API."}

def obtener_evaluaciones_api():
    url = f"{API_BASE_URL}/evaluaciones"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return {"exito": True, "evaluaciones": respuesta.json()}
        else:
            return {"exito": False, "evaluaciones": []}
    except requests.exceptions.RequestException:
        return {"exito": False, "evaluaciones": []}