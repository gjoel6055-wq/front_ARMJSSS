from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services import docente_service

docentes_bp = Blueprint("docentes", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@docentes_bp.route("/docentes")
def lista():
    redir = _requiere_login()
    if redir:
        return redir


    try:
        docentes = docente_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        docentes = []

    return render_template("docentes/lista.html", docentes=docentes)


@docentes_bp.route("/docentes/nuevo", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    if request.method == "POST":
        datos = {
            # Datos del usuario (backend hace doble insert)
            "email":        request.form.get("email"),
            "password":     request.form.get("password"),
            "nombre":       request.form.get("nombre"),
            "apellido":     request.form.get("apellido"),
            # Datos específicos del docente
            "departamento": request.form.get("departamento"),
        }
        try:
            docente_service.crear(datos)
            flash("Docente creado correctamente.", "success")
            return redirect(url_for("docentes.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("docentes/form.html", docente=None, accion="crear")


@docentes_bp.route("/docentes/<int:legajo>/editar", methods=["GET", "POST"])
def editar(legajo):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        docente = docente_service.obtener_por_legajo(legajo)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("docentes.lista"))

    if request.method == "POST":
        datos = {
            "nombre":       request.form.get("nombre"),
            "apellido":     request.form.get("apellido"),
            "departamento": request.form.get("departamento"),
        }
        try:
            docente_service.actualizar_parcial(legajo, datos)
            flash("Docente actualizado correctamente.", "success")
            return redirect(url_for("docentes.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("docentes/form.html", docente=docente, accion="editar")


@docentes_bp.route("/docentes/<int:legajo>/eliminar", methods=["POST"])
def eliminar(legajo):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        docente_service.eliminar(legajo)
        flash("Docente eliminado correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("docentes.lista"))