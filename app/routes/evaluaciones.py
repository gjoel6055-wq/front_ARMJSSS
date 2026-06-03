import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

evaluaciones_bp = Blueprint('evaluaciones', __name__)

BACKEND_URL = "http://localhost:5001/api"

@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
def listar_evaluaciones():
    token = session.get('token')
    
    if not token:
        flash("Debes iniciar sesión para ver las evaluaciones.", "error")
        return redirect(url_for('auth.login'))
        
    try:
        headers = {"Authorization": f"Bearer {token}"}
        respuesta = requests.get(f"{BACKEND_URL}/evaluaciones", headers=headers)
        
        if respuesta.status_code == 200:
            lista_de_evaluaciones = respuesta.json()
        else:
            lista_de_evaluaciones = []
            flash("No se pudieron cargar las evaluaciones.", "error")
            
    except requests.exceptions.RequestException:
        lista_de_evaluaciones = []
        flash("Error de conexión con el servidor backend.", "error")

    return render_template('evaluaciones/lista.html', evaluaciones=lista_de_evaluaciones)


@evaluaciones_bp.route('/evaluaciones/crear', methods=['GET'])
def formulario_crear():
    if not session.get('token'):
        flash("Debes iniciar sesión para planificar evaluaciones.", "error")
        return redirect(url_for('auth.login'))
        
    return render_template('evaluaciones/form.html', cursos=[], tipos=[])


@evaluaciones_bp.route('/evaluaciones/guardar', methods=['POST'])
def guardar_evaluacion():
    token = session.get('token')
    if not token:
        flash("Sesión expirada. Inicia sesión nuevamente.", "error")
        return redirect(url_for('auth.login'))

    datos_formulario = {
        "nombre": request.form.get("nombre"),
        "curso_id": int(request.form.get("curso_id")),
        "tipo_id": int(request.form.get("tipo_id")),
        "fecha": request.form.get("fecha"),
        "peso": float(request.form.get("peso"))
    }
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        respuesta = requests.post(f"{BACKEND_URL}/evaluaciones", json=datos_formulario, headers=headers)
        
        if respuesta.status_code == 201:
            flash("¡Evaluación planificada y creada con éxito!", "success")
            return redirect(url_for('evaluaciones.listar_evaluaciones'))
        else:
            error_msg = respuesta.json().get('error', 'Error desconocido.')
            flash(f"Error al crear: {error_msg}", "error")
            
    except requests.exceptions.RequestException:
        flash("No se pudo conectar con el backend para guardar la evaluación.", "error")
        
    return redirect(url_for('evaluaciones.formulario_crear'))
