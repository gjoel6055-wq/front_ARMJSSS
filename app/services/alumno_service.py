from app.services.api_client import get, post, put, delete


def obtener_alumnos():
    return get("/alumnos")


def obtener_alumno(id_alumno):
    return get(f"/alumnos/{id_alumno}")


def crear_alumno(datos):
    return post("/alumnos", json=datos)


def actualizar_alumno(id_alumno, datos):
    return put(f"/alumnos/{id_alumno}", json=datos)


def eliminar_alumno(id_alumno):
    return delete(f"/alumnos/{id_alumno}")