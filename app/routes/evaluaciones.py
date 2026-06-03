import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

evaluaciones_bp = Blueprint('evaluaciones', __name__)

BACKEND_URL = "http://localhost:5001/api"

@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
def listar_evaluaciones():
    if not session.get('token'):
        flash("Debes iniciar sesión para ver las evaluaciones.", "error")
        return redirect(url_for('auth.login'))

    if session.get('rol') != 'docente':
        flash("Acceso denegado: Solo los docentes pueden ver esta sección.", danger)
        return redirect(url_for('dashboard'))
        
    token = session.get('token')
    headers = {"Authorization": f"Bearer {token}"}
    
        
    try:
        respuesta = requests.get(f"{BACKEND_URL}/evaluaciones", headers=headers)
        if respuesta.status_code == 200:
            lista_de_evaluaciones = respuesta.json()
        else:
            lista_de_evaluaciones = []
            flash("No se pudieron cargar las evaluaciones desde el servidor.", "error")
     except requests.exceptions.RequestException:
        lista_de_evaluaciones = []
        flash("Error de conexión con el servidor backend.", "error")

    return render_template('evaluaciones/lista.html', evaluaciones=lista_de_evaluaciones)


@evaluaciones_bp.route('/evaluaciones/crear', methods=['GET'])
def crear_evaluacion():
    if not session.get('token'):
        flash("Debes iniciar sesión para crear evaluaciones.", "error")
        return redirect(url_for('auth.login'))
        
    return render_template('evaluaciones/form.html', cursos=[], tipos=[])

@evaluaciones_bp.route('/evaluaciones/crear', methods=['GET', 'POST'])
def crear_evaluacion():
    if not session.get('token'):
        flash("Debes iniciar sesión para crear evaluaciones.", "error")
        return redirect(url_for('auth.login'))

    if session.get('rol') != 'docente':
        flash("Acceso denegado: Solo los docentes pueden crear evaluaciones.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        datos_evaluacion = {
            'nombre': request.form['nombre'],
            'fecha': request.form['fecha'],
            'tipo': request.form['tipo']
        }

        token = session.get('token')
        headers = {"Authorization": f"Bearer {token}"}

        try:
            respuesta = requests.post(f"{BACKEND_URL}/evaluaciones", json=datos_evaluacion, headers=headers)
            if respuesta.status_code == 201:
                flash("¡Evaluación creada con éxito!", "success")
                return redirect(url_for('evaluaciones.listar_evaluaciones'))
            else:
                error_msg = respuesta.json().get('error', 'Error desconocido.')
                flash(f"Error al crear la evaluación: {error_msg}", "error")
        except requests.exceptions.RequestException:
            flash("Error de conexión con el servidor backend.", "error")

    return render_template('evaluaciones/form.html')
