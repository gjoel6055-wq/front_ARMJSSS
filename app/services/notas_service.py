from app.services.api_client import get, post, put, delete


def obtener_todas(evaluacion_id=None, padron=None):
    params = {}
    if evaluacion_id is not None:
        params["evaluacion_id"] = evaluacion_id
    if padron is not None:
        params["padron"] = padron
    return get("/notas", params=params)


def crear(datos):
    return post("/notas", json=datos)


def actualizar(nota_id, datos):
    return put(f"/notas/{nota_id}", json=datos)


def eliminar(nota_id):
    return delete(f"/notas/{nota_id}")
