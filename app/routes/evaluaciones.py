from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.evaluaciones_service import crear_evaluacion_api, obtener_tipos_y_cursos_api

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/evaluaciones', methods=['GET', 'POST'])
def listar_evaluaciones():
    if request.method == 'POST':
        datos_evaluacion = {
            'tipo_id': int(request.form['tipo_id']),
            'curso_id': int(request.form['curso_id']),
            'nombre': request.form['nombre'],
            'fecha': request.form['fecha'],
            'peso': float(request.form['peso']),
            'descripcion': request.form['descripcion']
        }
        
        resultado = crear_evaluacion_api(datos_evaluacion)
        
        if resultado['exito']:
            flash("¡Evaluación académica creada con éxito!", "success")
        else:
            flash(f"Error: {resultado.get('error')}", "danger")
            
        return redirect(url_for('evaluaciones.listar_evaluaciones'))

    datos_api = obtener_tipos_y_cursos_api()
    tipos = datos_api["tipos"] if datos_api["exito"] else []
    cursos = datos_api["cursos"] if datos_api["exito"] else []
        
    return render_template('evaluaciones/form.html', tipos=tipos, cursos=cursos)