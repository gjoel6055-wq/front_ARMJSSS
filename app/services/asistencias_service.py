import requests
from constants import API_BASE_URL


def disparar_envio_qr_api(token_usuario):
    url = f"{API_BASE_URL}/enviar_mails_asistencia"
    headers = {"Authorization": f"Bearer {token_usuario}"}

    try:
        respuesta = requests.post(url, headers=headers)

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

