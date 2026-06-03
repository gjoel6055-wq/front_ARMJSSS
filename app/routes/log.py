from flask import Blueprint, render_template, request, session, redirect, url_for
from app.services.log_service import obtener_logs_api, obtener_log_por_id_api

log_bp = Blueprint('log', __name__)


@log_bp.route('/historial_logs', methods=['GET'])
def index():
    token_usuario = session.get('token')
    rol_usuario = session.get('usuario_rol')

    if not token_usuario:
        return redirect(url_for('auth.login'))

    if rol_usuario != 'docente':
        return redirect(url_for('index'))

    accion_buscada = request.args.get('accion')

    filtros = {}
    if accion_buscada:
        filtros['accion'] = accion_buscada

    resultado = obtener_logs_api(token_usuario, filtros)

    if resultado['exito']:
        return render_template('log/lista.html', logs=resultado['datos'], accion_buscada=accion_buscada)
    else:
        return render_template('log/lista.html', error=resultado['error'], logs=[], accion_buscada=accion_buscada)


@log_bp.route('/detalle/<int:id>', methods=['GET'])
def detalle(id):
    token_usuario = session.get('token')
    if not token_usuario:
        return redirect(url_for('auth.login'))

    resultado = obtener_log_por_id_api(token_usuario, id)

    if resultado['exito']:
        return render_template('log/detalle.html', log=resultado['datos'])
    else:
        return redirect(url_for('log.index'))