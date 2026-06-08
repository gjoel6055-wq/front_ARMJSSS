from app.services.api_client import get


def obtener_todos():
    """GET /tipos-evaluacion — lista todos los tipos activos."""
    return get("/tipos-evaluacion")


def obtener_por_id(tipo_id):
    """GET /tipos-evaluacion/<id>"""
    return get(f"/tipos-evaluacion/{tipo_id}")
