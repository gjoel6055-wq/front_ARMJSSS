import requests
from app.constants import API_BASE_URL
import logging

logger = logging.getLogger(__name__)


def disparar_envio_qr_api(token_usuario, curso_id):
    url = f"{API_BASE_URL}/enviar_mails_asistencia"
    headers = {"Authorization": f"Bearer {token_usuario}"}
    payload = {"curso_id": curso_id}

    try:
        respuesta = requests.post(url, headers=headers, json=payload)

        if respuesta.status_code == 201:
            return {"exito": True, "datos": respuesta.json()}
        else:
            return {"exito": False, "error": "Error al procesar el envío masivo."}

    except requests.exceptions.RequestException:
        return {"exito": False, "error": "Error de conexión con la API."}


def asistencias_curso(fecha_buscada, token_usuario):
    url = f"{API_BASE_URL}/asistencias_curso"
    headers = {"Authorization": f"Bearer {token_usuario}"}
    parametros = {"fecha": fecha_buscada} if fecha_buscada else {}

    try:
        respuesta = requests.get(url,params=parametros, headers=headers)

        if respuesta.status_code == 200:
            return {"exito": True, "datos": respuesta.json()}
        else:
            return {"exito": False, "error": "Error al procesar el envío masivo."}

    except requests.exceptions.RequestException:
        return {"exito": False, "error": "Error de conexión con la API."}


def validar_asistencia_qr(token_qr, token_alumno):
    url_api = f"{API_BASE_URL}/asistencia/validar-qr/{token_qr}"

    headers = {
        'Authorization': f'Bearer {token_alumno}'
    }

    try:
        respuesta = requests.post(url_api, headers=headers)
        datos = respuesta.json()
        codigo_http = respuesta.status_code

        if codigo_http == 201:
            return {'estado': 'exito', 'mensaje': datos.get('mensaje')}

        elif codigo_http == 200:
            return {'estado': 'advertencia', 'mensaje': datos.get('mensaje')}

        else:
            return {'estado': 'error', 'mensaje': datos.get('error', 'Error al procesar el QR')}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con la API Backend: {e}")
        return {'estado': 'error', 'mensaje': 'Error de conexión con el servidor de la facultad.'}