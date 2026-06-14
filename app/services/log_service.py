import requests
from app.constants import API_BASE_URL
import logging

logger = logging.getLogger(__name__)

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
        logger.error(f"Error al traer logs: {e}")
        return {"exito": False, "error": "Error de conexión con la API."}
