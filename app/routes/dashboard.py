from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services.api_client import get

dashboard_bp = Blueprint("dashboard", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def index():
    redir = _requiere_login()
    if redir:
        return redir

    rol = session.get("usuario_rol")
    error = None

    if request.method == "POST":
        if rol != "docente":
            flash("No tenés permiso para cargar notas.", "danger")
            return redirect(url_for("dashboard.index"))

        tipo_carga = request.form.get("tipo_carga") 
        evaluacion_id = request.form.get("evaluacion_id")
        nota = request.form.get("nota")
        observacion = request.form.get("observacion", "")

        try:
            if tipo_carga == "grupal":
                equipo_id = request.form.get("equipo_id")
                post(
                    "/notas/grupal",
                    json={
                        "equipo_id": int(equipo_id),
                        "evaluacion_id": int(evaluacion_id),
                        "nota": float(nota),
                        "observacion": observacion,
                    },
                )
                flash("Nota grupal cargada correctamente.", "success")
            else:
                padron = request.form.get("padron")
                post(
                    "/notas",
                    json={
                        "padron": int(padron),
                        "evaluacion_id": int(evaluacion_id),
                        "nota": float(nota),
                        "observacion": observacion,
                    },
                )
                flash("Nota individual cargada correctamente.", "success")
        except Exception as e:
            flash(f"Error al cargar la nota: {str(e)}", "danger")

        return redirect(url_for("dashboard.index"))

    try:
        todas_notas = get("/notas")
        evaluaciones = get("/evaluaciones")
        equipos = get("/equipos")
        alumnos = get("/alumnos")
        stats_dashboard = get("/dashboard/estadisticas")
    except Exception as e:
        flash(f"Error al conectar con el servidor backend: {str(e)}", "danger")
        todas_notas, evaluaciones, equipos, alumnos = [], [], [], []
        stats_dashboard = {}

    total_gral = len(todas_notas)
    aprobados_gral = sum(1 for n in todas_notas if float(n.get("nota", 0)) >= 4.0)
    reprobados_gral = total_gral - aprobados_gral
    tasa_gral = (aprobados_gral / total_gral * 100) if total_gral > 0 else 0.0

    stats_gral = {
        "total": total_gral,
        "aprobados": aprobados_gral,
        "reprobados": reprobados_gral,
        "tasa_aprobacion": tasa_gral
    }

    stats_alumno = None
    mis_notas = []

    if rol == "alumno":
        email_sesion = session.get("usuario_email")
        alumno_actual = next(
            (a for a in alumnos if a.get("email") == email_sesion), None
        )
        if alumno_actual:
            padron_alumno = alumno_actual.get("padron")
            mis_notas = [n for n in todas_notas if n.get("padron") == padron_alumno]
            
            total_al = len(mis_notas)
            aprobados_al = sum(1 for n in mis_notas if float(n.get("nota", 0)) >= 4.0)
            reprobados_al = total_al - aprobados_al
            tasa_al = (aprobados_al / total_al * 100) if total_al > 0 else 0.0

            stats_alumno = {
                "total": total_al,
                "aprobados": aprobados_al,
                "reprobados": reprobados_al,
                "tasa_aprobacion": tasa_al
            }

    return render_template(
        "dashboard/dashboard.html",
        notas=todas_notas,
        mis_notas=mis_notas,
        evaluaciones=evaluaciones,
        equipos=equipos,
        alumnos=alumnos,
        rol=rol,
        stats_gral=stats_gral,
        stats_alumno=stats_alumno,
        stats_dashboard=stats_dashboard
    )
