from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from services import curso_service

cursos_bp = Blueprint("cursos", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@cursos_bp.route("/cursos")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    try:
        cursos = curso_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        cursos = []

    return render_template("cursos/lista.html", cursos=cursos)


@cursos_bp.route("/cursos/<int:curso_id>")
def detalle(curso_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        curso = curso_service.obtener_por_id(curso_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cursos.lista"))

    return render_template("cursos/detalle.html", curso=curso)


@cursos_bp.route("/cursos/nuevo", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    if request.method == "POST":
        datos = {
            "nombre":       request.form.get("nombre"),
            "cuatrimestre": request.form.get("cuatrimestre"),
            "anio":         request.form.get("anio"),
            "descripcion":  request.form.get("descripcion"),
        }
        try:
            curso_service.crear(datos)
            flash("Curso creado correctamente.", "success")
            return redirect(url_for("cursos.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("cursos/form.html", curso=None, accion="crear")


@cursos_bp.route("/cursos/<int:curso_id>/editar", methods=["GET", "POST"])
def editar(curso_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        curso = curso_service.obtener_por_id(curso_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cursos.lista"))

    if request.method == "POST":
        datos = {
            "nombre":       request.form.get("nombre"),
            "cuatrimestre": request.form.get("cuatrimestre"),
            "anio":         request.form.get("anio"),
            "descripcion":  request.form.get("descripcion"),
        }
        try:
            curso_service.actualizar(curso_id, datos)
            flash("Curso actualizado correctamente.", "success")
            return redirect(url_for("cursos.detalle", curso_id=curso_id))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("cursos/form.html", curso=curso, accion="editar")


@cursos_bp.route("/cursos/<int:curso_id>/eliminar", methods=["POST"])
def eliminar(curso_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        curso_service.eliminar(curso_id)
        flash("Curso eliminado correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("cursos.lista"))