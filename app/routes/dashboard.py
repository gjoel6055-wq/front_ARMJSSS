from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services.api_client import get

dashboard_bp = Blueprint("dashboard", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@dashboard_bp.route("/dashboard", methods=["GET"])
def index():
    redir = _requiere_login()
    if redir:
        return redir

    rol = session.get("usuario_rol")

    try:
        todas_notas = get("/notas") or []
    except Exception:
        todas_notas = []

    try:
        cursos = get("/cursos") or []
    except Exception:
        cursos = []

    try:
        stats_dashboard = get("/dashboard/estadisticas") or {}
    except Exception:
        stats_dashboard = {}

    filtro_curso = request.args.get("curso_id", "")

    notas_filtradas = todas_notas
    if filtro_curso:
        notas_filtradas = [n for n in notas_filtradas if str(n.get("curso_id")) == filtro_curso]

    total = len(notas_filtradas)
    aprobados = sum(1 for n in notas_filtradas if float(n.get("nota", 0)) >= 4)
    reprobados = total - aprobados
    tasa = (aprobados / total * 100) if total else 0
    stats_gral = {
        "total": total,
        "aprobados": aprobados,
        "reprobados": reprobados,
        "tasa_aprobacion": tasa,
    }

    rol = session.get("usuario_rol")
    padron = session.get("padron")
    stats_alumno = None
    mis_notas = []
    if rol == "alumno" and padron:
        mis_notas = [n for n in notas_filtradas if str(n.get("padron")) == str(padron)]
        total_mias = len(mis_notas)
        aprobadas_mias = sum(1 for n in mis_notas if float(n.get("nota", 0)) >= 4)
        stats_alumno = {
            "total": total_mias,
            "aprobados": aprobadas_mias,
            "reprobados": total_mias - aprobadas_mias,
            "tasa_aprobacion": (aprobadas_mias / total_mias * 100) if total_mias else 0,
        }

    return render_template(
        "dashboard/dashboard.html",
        notas=notas_filtradas,
        mis_notas=mis_notas,
        stats_gral=stats_gral,
        stats_alumno=stats_alumno,
        stats_dashboard=stats_dashboard,
        rol=rol,
        cursos=cursos,
        filtro_curso=filtro_curso,
    )
