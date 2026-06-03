from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.services import equipo_service, curso_service

equipos_bp = Blueprint("equipos", __name__)


def _requiere_login():
    """Redirige al login si no hay token en sesión."""
    if not session.get("token"):
        flash("Debés iniciar sesión para acceder.", "warning")
        return redirect(url_for("auth.login"))
    return None


@equipos_bp.route("/equipos")
def lista():
    redir = _requiere_login()
    if redir:
        return redir

    curso_id = request.args.get("curso_id", type=int)

    try:
        equipos = equipo_service.obtener_todos(curso_id=curso_id)
        cursos  = curso_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        equipos, cursos = [], []

    return render_template(
        "equipos/lista.html",
        equipos=equipos,
        cursos=cursos,
        curso_id_activo=curso_id,
    )


@equipos_bp.route("/equipos/<int:equipo_id>")
def detalle(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        equipo = equipo_service.obtener_por_id(equipo_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipos.lista"))

    return render_template("equipos/detalle.html", equipo=equipo)


@equipos_bp.route("/equipos/nuevo", methods=["GET", "POST"])
def crear():
    redir = _requiere_login()
    if redir:
        return redir

    try:
        cursos = curso_service.obtener_todos()
    except ValueError:
        cursos = []

    if request.method == "POST":
        datos = {
            "nombre":   request.form.get("nombre"),
            "curso_id": request.form.get("curso_id"),
        }
        try:
            equipo = equipo_service.crear(datos)
            flash("Equipo creado correctamente.", "success")
            return redirect(url_for("equipos.detalle", equipo_id=equipo["equipo_id"]))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("equipos/form.html", equipo=None, cursos=cursos, accion="crear")


@equipos_bp.route("/equipos/<int:equipo_id>/editar", methods=["GET", "POST"])
def editar(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        equipo = equipo_service.obtener_por_id(equipo_id)
        cursos = curso_service.obtener_todos()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipos.lista"))

    if request.method == "POST":
        datos = {
            "nombre":   request.form.get("nombre"),
            "curso_id": request.form.get("curso_id"),
        }
        try:
            equipo_service.actualizar(equipo_id, datos)
            flash("Equipo actualizado correctamente.", "success")
            return redirect(url_for("equipos.detalle", equipo_id=equipo_id))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("equipos/form.html", equipo=equipo, cursos=cursos, accion="editar")


@equipos_bp.route("/equipos/<int:equipo_id>/eliminar", methods=["POST"])
def eliminar(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    try:
        equipo_service.eliminar(equipo_id)
        flash("Equipo eliminado correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipos.lista"))


@equipos_bp.route("/equipos/<int:equipo_id>/alumnos/agregar", methods=["POST"])
def agregar_alumno(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    padron = request.form.get("padron", type=int)
    try:
        equipo_service.agregar_alumno(equipo_id, padron)
        flash("Alumno agregado al equipo.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipos.detalle", equipo_id=equipo_id))


@equipos_bp.route("/equipos/<int:equipo_id>/alumnos/quitar", methods=["POST"])
def quitar_alumno(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    padron = request.form.get("padron", type=int)
    try:
        equipo_service.quitar_alumno(equipo_id, padron)
        flash("Alumno quitado del equipo.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipos.detalle", equipo_id=equipo_id))


@equipos_bp.route("/equipos/<int:equipo_id>/evaluaciones/agregar", methods=["POST"])
def agregar_evaluacion(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    evaluacion_id = request.form.get("evaluacion_id", type=int)
    try:
        equipo_service.agregar_evaluacion(equipo_id, evaluacion_id)
        flash("Evaluación agregada al equipo.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipos.detalle", equipo_id=equipo_id))


@equipos_bp.route("/equipos/<int:equipo_id>/evaluaciones/quitar", methods=["POST"])
def quitar_evaluacion(equipo_id):
    redir = _requiere_login()
    if redir:
        return redir

    evaluacion_id = request.form.get("evaluacion_id", type=int)
    try:
        equipo_service.quitar_evaluacion(equipo_id, evaluacion_id)
        flash("Evaluación quitada del equipo.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipos.detalle", equipo_id=equipo_id))