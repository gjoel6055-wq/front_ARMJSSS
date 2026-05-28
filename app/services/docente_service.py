from app.services.api_client import get, post, put, patch, delete


def obtener_todos():
    """GET /docentes — lista todos los docentes activos."""
    return get("/docentes")


def obtener_por_legajo(legajo):
    """GET /docentes/<legajo> — detalle de un docente."""
    return get(f"/docentes/{legajo}")


def crear(datos):
    """
    POST /docentes
    datos esperados: { email, password, nombre, apellido, departamento }
    El backend crea primero el usuario y luego el docente.
    """
    return post("/docentes", json=datos)


def actualizar(legajo, datos):
    """PUT /docentes/<legajo> — reemplaza todos los campos del docente."""
    return put(f"/docentes/{legajo}", json=datos)


def actualizar_parcial(legajo, datos):
    """PATCH /docentes/<legajo> — actualiza solo los campos enviados."""
    return patch(f"/docentes/{legajo}", json=datos)


def eliminar(legajo):
    """DELETE /docentes/<legajo> — borrado lógico (deleted_at)."""
    return delete(f"/docentes/{legajo}")