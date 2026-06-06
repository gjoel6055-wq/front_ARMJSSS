from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services import alumno_service

alumnos_bp = Blueprint("alumnos", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@alumnos_bp.route("/alumnos")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    try:
        alumnos = alumno_service.obtener_alumnos()
    except ValueError as e:
        flash(str(e), "danger")
        alumnos = []

    return render_template("alumnos/lista.html", alumnos=alumnos)


@alumnos_bp.route("/alumnos/<int:id>")
def detalle(id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        alumno = alumno_service.obtener_alumno(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("alumnos.lista"))

    return render_template("alumnos/detalle.html", alumno=alumno)


@alumnos_bp.route("/alumnos/nuevo", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    if request.method == "POST":
        datos = {
            "padron":    request.form.get("padron"),
            "nombre":    request.form.get("nombre"),
            "apellido":  request.form.get("apellido"),
            "email":     request.form.get("email"),
            "password":  request.form.get("password"),
            "abandono":  request.form.get("abandono") == "1",
        }
        try:
            alumno_service.crear_alumno(datos)
            flash("Alumno creado correctamente.", "success")
            return redirect(url_for("alumnos.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("alumnos/form.html", alumno=None, accion="crear")


@alumnos_bp.route("/alumnos/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    redir = _requiere_login()
    if redir:
        return redir

    from services import curso_service
    try:
        alumno = alumno_service.obtener_alumno(id)
        cursos_disponibles = curso_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("alumnos.lista"))

    if request.method == "POST":
        datos = {
            "nombre":   request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "email":    request.form.get("email"),
            "abandono": request.form.get("abandono") == "1",
            "cursos":   request.form.getlist("cursos")
        }
        password = request.form.get("password")
        if password:
            datos["password"] = password
        try:
            alumno_service.actualizar_alumno(id, datos)
            flash("Alumno actualizado correctamente.", "success")
            return redirect(url_for("alumnos.detalle", id=id))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("alumnos/form.html", alumno=alumno, accion="editar", cursos_disponibles=cursos_disponibles)


@alumnos_bp.route("/alumnos/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        alumno_service.eliminar_alumno(id)
        flash("Alumno eliminado correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("alumnos.lista"))