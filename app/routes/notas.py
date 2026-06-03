import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

notas_bp = Blueprint('notas', __name__)

BACKEND_URL = "http://localhost:5001/api"

@notas_bp.route('/notas', methods=['GET', 'POST'])
def listar_notas():
    if not session.get('token'):
        flash("Debes iniciar sesión para gestionar las notas.", "error")
        return redirect(url_for('auth.login'))

    token = session.get('token')
    headers = {"Authorization": f"Bearer {token}"}

    if request.method == 'POST':
        datos_nota = {
            'padron': int(request.form['padron']),
            'evaluacion_id': int(request.form['evaluacion_id']),
            'nota': float(request.form['nota'])
        }
        
        try:
            respuesta = requests.post(f"{BACKEND_URL}/notas", json=datos_nota, headers=headers)
            
            if respuesta.status_code == 201:
                flash("¡Nota registrada con éxito!", "success")
            else:
                error_msg = respuesta.json().get('error', 'Error desconocido.')
                flash(f"Error al cargar la nota: {error_msg}", "error")
                
        except requests.exceptions.RequestException:
            flash("Error de conexión con el servidor backend al guardar.", "error")
            
        return redirect(url_for('notas.listar_notas'))

    try:
        respuesta_evaluaciones = requests.get(f"{BACKEND_URL}/evaluaciones", headers=headers)
        if respuesta_evaluaciones.status_code == 200:
            evaluaciones = respuesta_evaluaciones.json()
        else:
            evaluaciones = []
            flash("No se pudieron cargar las evaluaciones para el formulario.", "error")
            
    except requests.exceptions.RequestException:
        evaluaciones = []
        flash("Error de conexión con el backend. Mostrando datos de respaldo.", "error")
        
    return render_template('notas/form.html', evaluaciones=evaluaciones)
