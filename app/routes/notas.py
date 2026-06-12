from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services.notas_service import obtener_todas, crear, actualizar, eliminar as eliminar_nota
from app.services.evaluacion_service import obtener_todas as obtener_evaluaciones
from app.services.alumno_service import obtener_alumnos

notas_bp = Blueprint("notas", __name__)


def _requiere_login():
    """Redirige al login si no hay sesión activa."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


def _requiere_docente():
    """Redirige si no hay sesión o el rol no es docente."""
    redir = _requiere_login()
    if redir:
        return redir
    if session.get("usuario_rol") != "docente":
        flash("No tenés permiso para realizar esa acción.", "danger")
        return redirect(url_for("notas.lista"))
    return None


@notas_bp.route("/notas")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    es_docente = session.get("usuario_rol") == "docente"
    evaluacion_id = request.args.get("evaluacion_id", type=int)

    try:
        notas = obtener_todas(evaluacion_id=evaluacion_id)
        evaluaciones = obtener_evaluaciones()
    except ValueError as e:
        flash(str(e), "danger")
        notas, evaluaciones = [], []

    return render_template(
        "notas/lista.html",
        notas=notas,
        evaluaciones=evaluaciones,
        evaluacion_id_activo=evaluacion_id,
        es_docente=es_docente,
    )


@notas_bp.route("/notas/nueva", methods=["GET", "POST"])
def crear_nota():
    redir = _requiere_docente()
    if redir:
        return redir

    try:
        evaluaciones = obtener_evaluaciones()
        alumnos = obtener_alumnos()
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
            crear(datos)
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
    redir = _requiere_docente()
    if redir:
        return redir

    try:
        evaluaciones = obtener_evaluaciones()
        alumnos = obtener_alumnos()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("notas.lista"))

    nota = None
    try:
        todas = obtener_todas()
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
            actualizar(nota_id, datos)
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
    redir = _requiere_docente()
    if redir:
        return redir

    try:
        eliminar_nota(nota_id)
        flash("Nota eliminada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("notas.lista"))
