from app.services.api_client import get, post, put, patch, delete

def obtener_todos(curso_id=None):
    params = {}
    if curso_id is not None:
        params["curso_id"] = curso_id
    return get("/equipos", params=params)

def obtener_por_id(equipo_id):
    return get(f"/equipos/{equipo_id}")

def crear(datos):
    return post("/equipos", json=datos)

def actualizar(equipo_id, datos):
    return put(f"/equipos/{equipo_id}", json=datos)

def actualizar_parcial(equipo_id, datos):
    return patch(f"/equipos/{equipo_id}", json=datos)

def eliminar(equipo_id):
    return delete(f"/equipos/{equipo_id}")

def agregar_alumno(equipo_id, padron):
    return post(f"/equipos/{equipo_id}/alumnos", json={"padron": padron})

def quitar_alumno(equipo_id, padron):
    return delete(f"/equipos/{equipo_id}/alumnos/{padron}")

def agregar_evaluacion(equipo_id, evaluacion_id):
    return post(f"/equipos/{equipo_id}/evaluaciones", json={"evaluacion_id": evaluacion_id})

def quitar_evaluacion(equipo_id, evaluacion_id):
    return delete(f"/equipos/{equipo_id}/evaluaciones/{evaluacion_id}")