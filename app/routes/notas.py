from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services import nota_service, evaluacion_service, alumno_service

notas_bp = Blueprint("notas", __name__)


def _requiere_login():
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@notas_bp.route("/notas")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    evaluacion_id = request.args.get("evaluacion_id", type=int)

    try:
        notas = nota_service.obtener_todas(evaluacion_id=evaluacion_id)
        evaluaciones = evaluacion_service.obtener_todas()
    except ValueError as e:
        flash(str(e), "danger")
        notas, evaluaciones = [], []

    return render_template(
        "notas/lista.html",
        notas=notas,
        evaluaciones=evaluaciones,
        evaluacion_id_activo=evaluacion_id,
    )


@notas_bp.route("/notas/nueva", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    try:
        evaluaciones = evaluacion_service.obtener_todas()
        alumnos = alumno_service.obtener_todos()
    except ValueError:
        evaluaciones, alumnos = [], []

    if request.method == "POST":
        datos = {
            "padron":        request.form.get("padron", type=int),
            "evaluacion_id": request.form.get("evaluacion_id", type=int),
            "nota":          request.form.get("nota", type=float),
            "observacion":   request.form.get("observacion"),
        }
        try:
            nota_service.crear(datos)
            flash("Nota cargada correctamente.", "success")
            return redirect(url_for("notas.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "notas/form.html",
        nota=None,
        evaluaciones=evaluaciones,
        alumnos=alumnos,
        accion="crear",
    )


@notas_bp.route("/notas/<int:nota_id>/editar", methods=["GET", "POST"])
def editar(nota_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        evaluaciones = evaluacion_service.obtener_todas()
        alumnos = alumno_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("notas.lista"))

    # Buscamos la nota en la lista para precargar el form
    nota = None
    try:
        todas = nota_service.obtener_todas()
        nota = next((n for n in todas if n["nota_id"] == nota_id), None)
    except ValueError:
        pass

    if nota is None:
        flash("Nota no encontrada.", "danger")
        return redirect(url_for("notas.lista"))

    if request.method == "POST":
        datos = {
            "padron":        request.form.get("padron", type=int),
            "evaluacion_id": request.form.get("evaluacion_id", type=int),
            "nota":          request.form.get("nota", type=float),
            "observacion":   request.form.get("observacion"),
        }
        try:
            nota_service.actualizar(nota_id, datos)
            flash("Nota actualizada correctamente.", "success")
            return redirect(url_for("notas.lista"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "notas/form.html",
        nota=nota,
        evaluaciones=evaluaciones,
        alumnos=alumnos,
        accion="editar",
    )


@notas_bp.route("/notas/<int:nota_id>/eliminar", methods=["POST"])
def eliminar(nota_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        nota_service.eliminar(nota_id)
        flash("Nota eliminada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("notas.lista"))
