import requests
from constants import API_BASE_URL

def crear_evaluacion_api(datos_evaluacion):
    url = f"{API_BASE_URL}/evaluaciones"
    try:
        respuesta = requests.post(url, json=datos_evaluacion)
        if respuesta.status_code == 201:
            return {"exito": True, "datos": respuesta.json()}
        else:
            return {"exito": False, "error": "Error al procesar la creación masiva."}
    except requests.exceptions.RequestException:
        return {"exito": False, "error": "Error de conexión con la API."}

def obtener_tipos_y_cursos_api():
    url_tipos = f"{API_BASE_URL}/tipos_evaluacion"
    url_cursos = f"{API_BASE_URL}/cursos"
    resultado = {"exito": True, "tipos": [], "cursos": []}
    
    try:
        res_tipos = requests.get(url_tipos)
        res_cursos = requests.get(url_cursos)
        
        if res_tipos.status_code == 200 and res_cursos.status_code == 200:
            resultado["tipos"] = res_tipos.json()
            resultado["cursos"] = res_cursos.json()
        else:
            resultado["exito"] = False
    except requests.exceptions.RequestException:
        resultado["exito"] = False
        
    return resultado