import requests
from app.constants import API_BASE_URL


def obtener_logs_api(token_usuario, filtros=None):
    url = f"{API_BASE_URL}/historial_logs"
    headers = {"Authorization": f"Bearer {token_usuario}"}

    try:
        respuesta = requests.get(url, headers=headers, params=filtros)

        if respuesta.status_code == 200:
            datos_json = respuesta.json()
            lista_historial = datos_json.get('historial', [])
            return {"exito": True, "datos": lista_historial}
        else:
            mensaje_error = respuesta.json().get('error', 'Error al obtener historial.')
            return {"exito": False, "error": mensaje_error}

    except requests.exceptions.RequestException as e:
        print(f"Error al traer logs: {e}")
        return {"exito": False, "error": "Error de conexión con la API."}


def obtener_log_por_id_api(token_usuario, id_log):
    url = f"{API_BASE_URL}/logs/{id_log}"
    headers = {"Authorization": f"Bearer {token_usuario}"}

    try:
        respuesta = requests.get(url, headers=headers)
        if respuesta.status_code == 200:
            return {"exito": True, "datos": respuesta.json().get('log')}
        else:
            return {"exito": False, "error": respuesta.json().get('error')}
    except requests.exceptions.RequestException:
        return {"exito": False, "error": "Error de conexión con la API."}