import requests
from constants import API_BASE_URL


def hacer_login(email, password):
    url = f"{API_BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }

    try:
        respuesta = requests.post(url, json=payload)
        datos_api = respuesta.json()

        if respuesta.status_code == 200:
            return {"exito": True, "datos": datos_api}

        else:

            mensaje_error = datos_api.get('error', 'Error desconocido en el servidor.')
            return {"exito": False, "error": mensaje_error}

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return {"exito": False, "error": "Error de conexión con la API. Intentá más tarde."}


def hacer_logout(token):
    url = f"{API_BASE_URL}/auth/logout"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        respuesta = requests.post(url, headers=headers)

        if respuesta.status_code == 200:
            return True
        return False

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al cerrar sesión en la API: {e}")
        return False