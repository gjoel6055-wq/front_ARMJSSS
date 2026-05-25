from flask import Blueprint, render_template

asistencias_bp = Blueprint('asistencias', __name__)

@asistencias_bp.route('/')
def index():
    return render_template('asistencias/lista.html')

@asistencias_bp.route('/validar/<token>')
def validar(token):
    return render_template('asistencias/validar.html', token=token)

@asistencias_bp.route('/generar')
def generar():
    return render_template('asistencias/generar.html')