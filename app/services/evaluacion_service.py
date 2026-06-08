from app.services.api_client import get, post, put, patch, delete


def obtener_todas(curso_id=None):
    """GET /evaluaciones — lista todas las evaluaciones, opcionalmente filtradas por curso."""
    params = {}
    if curso_id is not None:
        params["curso_id"] = curso_id
    return get("/evaluaciones", params=params)


def obtener_por_id(evaluacion_id):
    """GET /evaluaciones/<id> — detalle de una evaluación."""
    return get(f"/evaluaciones/{evaluacion_id}")


def crear(datos):
    """
    POST /evaluaciones
    datos esperados: { nombre, tipo_id, curso_id, fecha, peso, descripcion }
    """
    return post("/evaluaciones", json=datos)


def actualizar(evaluacion_id, datos):
    """PUT /evaluaciones/<id> — reemplaza todos los campos."""
    return put(f"/evaluaciones/{evaluacion_id}", json=datos)


def actualizar_parcial(evaluacion_id, datos):
    """PATCH /evaluaciones/<id> — actualiza solo los campos enviados."""
    return patch(f"/evaluaciones/{evaluacion_id}", json=datos)


def eliminar(evaluacion_id):
    """DELETE /evaluaciones/<id> — borrado lógico."""
    return delete(f"/evaluaciones/{evaluacion_id}")
