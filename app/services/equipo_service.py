from app.services.api_client import get, post, put, patch, delete


# ── CRUD principal ──────────────────────────────────────────────────────────

def obtener_todos(curso_id=None):
    """
    GET /equipos — lista todos los equipos.
    Si se pasa curso_id filtra por ese curso: GET /equipos?curso_id=<id>
    """
    params = {}
    if curso_id is not None:
        params["curso_id"] = curso_id
    return get("/equipos", params=params)


def obtener_por_id(equipo_id):
    """GET /equipos/<id> — detalle con alumnos y evaluaciones asociadas."""
    return get(f"/equipos/{equipo_id}")


def crear(datos):
    """
    POST /equipos
    datos esperados: { nombre, curso_id }
    """
    return post("/equipos", json=datos)


def actualizar(equipo_id, datos):
    """PUT /equipos/<id> — reemplaza todos los campos del equipo."""
    return put(f"/equipos/{equipo_id}", json=datos)


def actualizar_parcial(equipo_id, datos):
    """PATCH /equipos/<id> — actualiza solo los campos enviados."""
    return patch(f"/equipos/{equipo_id}", json=datos)


def eliminar(equipo_id):
    """DELETE /equipos/<id> — borrado lógico + elimina pivots."""
    return delete(f"/equipos/{equipo_id}")


# ── Gestión de alumnos en el equipo ────────────────────────────────────────

def agregar_alumno(equipo_id, padron):
    """
    POST /equipos/<id>/alumnos
    datos esperados: { padron }
    """
    return post(f"/equipos/{equipo_id}/alumnos", json={"padron": padron})


def quitar_alumno(equipo_id, padron):
    """
    DELETE /equipos/<id>/alumnos
    datos esperados: { padron }
    """
    return delete(f"/equipos/{equipo_id}/alumnos", json={"padron": padron})


# ── Gestión de evaluaciones en el equipo ───────────────────────────────────

def agregar_evaluacion(equipo_id, evaluacion_id):
    """
    POST /equipos/<id>/evaluaciones
    datos esperados: { evaluacion_id }
    """
    return post(
        f"/equipos/{equipo_id}/evaluaciones",
        json={"evaluacion_id": evaluacion_id},
    )


def quitar_evaluacion(equipo_id, evaluacion_id):
    """
    DELETE /equipos/<id>/evaluaciones
    datos esperados: { evaluacion_id }
    """
    return delete(
        f"/equipos/{equipo_id}/evaluaciones",
        json={"evaluacion_id": evaluacion_id},
    )