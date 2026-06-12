from app.constants import API_BASE_URL
import requests
from flask import session


def _headers():
    """Construye los headers comunes; incluye Authorization si hay token en sesión."""
    headers = {"Content-Type": "application/json"}
    token = session.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _url(path: str) -> str:
    """Concatena la base con el path, asegurando una sola barra."""
    return API_BASE_URL + "/" + path.lstrip("/")


def _manejar_respuesta(response: requests.Response):
    """
    Devuelve el JSON parseado si el status es 2xx.
    Lanza ValueError con el mensaje del backend para cualquier error >= 400.
    """
    if response.ok:
        if response.status_code == 204:
            return None
        return response.json()

    # Intentar extraer el mensaje de error del backend
    try:
        payload = response.json()
        mensaje = payload.get("error") or payload.get("mensaje") or response.text
    except Exception:
        mensaje = response.text or f"Error HTTP {response.status_code}"

    raise ValueError(mensaje)


def get(path: str, params: dict = None):
    """Realiza un GET al backend y devuelve el JSON de la respuesta."""
    response = requests.get(
        _url(path),
        headers=_headers(),
        params=params,
        timeout=TIMEOUT,
    )
    return _manejar_respuesta(response)


def post(path: str, json: dict = None):
    """Realiza un POST al backend y devuelve el JSON de la respuesta."""
    response = requests.post(
        _url(path),
        headers=_headers(),
        json=json,
        timeout=TIMEOUT,
    )
    return _manejar_respuesta(response)


def put(path: str, json: dict = None):
    """Realiza un PUT al backend y devuelve el JSON de la respuesta."""
    response = requests.put(
        _url(path),
        headers=_headers(),
        json=json,
        timeout=TIMEOUT,
    )
    return _manejar_respuesta(response)


def patch(path: str, json: dict = None):
    """Realiza un PATCH al backend y devuelve el JSON de la respuesta."""
    response = requests.patch(
        _url(path),
        headers=_headers(),
        json=json,
        timeout=TIMEOUT,
    )
    return _manejar_respuesta(response)


def delete(path: str, json: dict = None):
    """Realiza un DELETE al backend y devuelve el JSON de la respuesta (puede ser None)."""
    response = requests.delete(
        _url(path),
        headers=_headers(),
        json=json,
        timeout=TIMEOUT,
    )
    return _manejar_respuesta(response)