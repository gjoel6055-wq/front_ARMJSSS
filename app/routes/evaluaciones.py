from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services import evaluacion_service, curso_service, tipo_evaluacion_service

evaluaciones_bp = Blueprint("evaluaciones", __name__)


def _requiere_login():
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@evaluaciones_bp.route("/evaluaciones")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    curso_id = request.args.get("curso_id", type=int)

    try:
        evaluaciones = evaluacion_service.obtener_todas(curso_id=curso_id)
        cursos       = curso_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        evaluaciones, cursos = [], []

    return render_template(
        "evaluaciones/lista.html",
        evaluaciones=evaluaciones,
        cursos=cursos,
        curso_id_activo=curso_id,
    )


@evaluaciones_bp.route("/evaluaciones/<int:evaluacion_id>")
def detalle(evaluacion_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        evaluacion = evaluacion_service.obtener_por_id(evaluacion_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("evaluaciones.lista"))

    return render_template("evaluaciones/detalle.html", evaluacion=evaluacion)


@evaluaciones_bp.route("/evaluaciones/nueva", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    try:
        cursos = curso_service.obtener_todos()
        tipos  = tipo_evaluacion_service.obtener_todos()
    except ValueError:
        cursos, tipos = [], []

    if request.method == "POST":
        datos = {
            "nombre":      request.form.get("nombre"),
            "tipo_id":     request.form.get("tipo_id", type=int),
            "curso_id":    request.form.get("curso_id", type=int),
            "fecha":       request.form.get("fecha"),
            "peso":        request.form.get("peso", type=float),
            "descripcion": request.form.get("descripcion"),
        }
        try:
            evaluacion = evaluacion_service.crear(datos)
            flash("Evaluación creada correctamente.", "success")
            return redirect(url_for("evaluaciones.detalle", evaluacion_id=evaluacion["evaluacion_id"]))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "evaluaciones/form.html",
        evaluacion=None,
        cursos=cursos,
        tipos=tipos,
        accion="crear",
    )


@evaluaciones_bp.route("/evaluaciones/<int:evaluacion_id>/editar", methods=["GET", "POST"])
def editar(evaluacion_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        evaluacion = evaluacion_service.obtener_por_id(evaluacion_id)
        cursos     = curso_service.obtener_todos()
        tipos      = tipo_evaluacion_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("evaluaciones.lista"))

    if request.method == "POST":
        datos = {
            "nombre":      request.form.get("nombre"),
            "tipo_id":     request.form.get("tipo_id", type=int),
            "curso_id":    request.form.get("curso_id", type=int),
            "fecha":       request.form.get("fecha"),
            "peso":        request.form.get("peso", type=float),
            "descripcion": request.form.get("descripcion"),
        }
        try:
            evaluacion_service.actualizar(evaluacion_id, datos)
            flash("Evaluación actualizada correctamente.", "success")
            return redirect(url_for("evaluaciones.detalle", evaluacion_id=evaluacion_id))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "evaluaciones/form.html",
        evaluacion=evaluacion,
        cursos=cursos,
        tipos=tipos,
        accion="editar",
    )


@evaluaciones_bp.route("/evaluaciones/<int:evaluacion_id>/eliminar", methods=["POST"])
def eliminar(evaluacion_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        evaluacion_service.eliminar(evaluacion_id)
        flash("Evaluación eliminada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("evaluaciones.lista"))
