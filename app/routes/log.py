from flask import Blueprint, render_template

log_bp = Blueprint('log', __name__)

@log_bp.route('/historial_logs')
def index():
    return render_template('log/lista.html')

@log_bp.route('/detalle/<int:id>')
def detalle(id):
    return render_template('log/detalle.html', log_id=id)