from services.api_client import get, post, put, patch, delete


def obtener_todos():
    """GET /cursos — lista todos los cursos activos."""
    return get("/cursos")


def obtener_por_id(curso_id):
    """GET /cursos/<id> — detalle de un curso."""
    return get(f"/cursos/{curso_id}")


def crear(datos):
    """
    POST /cursos
    datos esperados: { nombre, cuatrimestre, anio, descripcion }
    """
    return post("/cursos", json=datos)


def actualizar(curso_id, datos):
    """PUT /cursos/<id> — reemplaza todos los campos del curso."""
    return put(f"/cursos/{curso_id}", json=datos)


def actualizar_parcial(curso_id, datos):
    """PATCH /cursos/<id> — actualiza solo los campos enviados."""
    return patch(f"/cursos/{curso_id}", json=datos)


def eliminar(curso_id):
    """DELETE /cursos/<id> — borrado lógico (deleted_at)."""
    return delete(f"/cursos/{curso_id}")