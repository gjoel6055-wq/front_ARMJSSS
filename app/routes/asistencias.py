from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.asistencias_service import disparar_envio_qr_api, asistencias_curso, validar_asistencia_qr
from datetime import datetime
asistencias_bp = Blueprint("asistencia", __name__)


@asistencias_bp.route('/', methods=['GET','POST'])
def index():
    return render_template('asistencias/lista.html')


@asistencias_bp.route('/generar', methods=['GET', 'POST'])
def generar():
    token = session.get('token')

    resultado = disparar_envio_qr_api(token)

    if resultado['exito']:
        flash("¡Éxito! Se enviaron los QRs para la clase de hoy.", "success")
    else:
        flash(f"Error: {resultado['error']}", "danger")

    hoy_str = datetime.now().strftime('%Y-%m-%d')
    return redirect(url_for('asistencia.fecha_clase', fecha=hoy_str))

@asistencias_bp.route('/asistencias_curso', methods=['GET'])
def fecha_clase():
    token = session.get("token")
    fecha_param = request.args.get('fecha')
    resultado = asistencias_curso(fecha_param, token)

    if not fecha_param:
        fecha = datetime.now().strftime('%Y-%m-%d')
    else:
        fecha = fecha_param

    if resultado['exito']:

        lista_alumnos = resultado['datos'].get('lista_alumnos', [])

        return render_template('asistencias/lista.html', alumnos=lista_alumnos, fecha_actual=fecha)
    else:
        return render_template('asistencias/lista.html', error=resultado['error'], fecha_actual=fecha)


@asistencias_bp.route('/validar/<string:token>', methods=['GET'])
def vista_escanear_qr(token):
    token_alumno = session.get('token')


    if not token_alumno:
        return redirect('/login')

    resultado = validar_asistencia_qr(token, token_alumno)

    return render_template('asistencias/validar.html',
                           estado=resultado['estado'],
                           mensaje=resultado['mensaje'])
