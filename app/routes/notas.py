from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.notas_service import registrar_nota_api, obtener_evaluaciones_api

notas_bp = Blueprint('notas', __name__)

@notas_bp.route('/notas', methods=['GET', 'POST'])
def listar_notas():
    if request.method == 'POST':
        datos_nota = {
            'padron': int(request.form['padron']),
            'evaluacion_id': int(request.form['evaluacion_id']),
            'nota': float(request.form['nota']),
            'observacion': request.form['observacion']
        }
        
        resultado = registrar_nota_api(datos_nota)
        
        if resultado['exito']:
            flash("¡Nota registrada con éxito!", "success")
        else:
            flash(f"Error: {resultado.get('error')}", "danger")
            
        return redirect(url_for('notas.listar_notas'))

    resultado_api = obtener_evaluaciones_api()
    evaluaciones = resultado_api["evaluaciones"]
        
    return render_template('notas/form.html', evaluaciones=evaluaciones)