from flask import Flask, render_template
from app.routes.auth import auth_bp
from app.routes.asistencias import asistencias_bp
from app.routes.log import log_bp
from app.routes.docentes import docentes_bp
from app.routes.equipos import equipos_bp
from app.routes.cursos import cursos_bp
from app.routes.alumnos import alumnos_bp
from app.routes.dashboard import dashboard_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.secret_key = 'una_clave_super_secreta_para_fiuba_2026'

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(log_bp, url_prefix='/log')
app.register_blueprint(asistencias_bp, url_prefix='/asistencia')
app.register_blueprint(docentes_bp, url_prefix='/docentes')
app.register_blueprint(equipos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(dashboard_bp)


@app.route('/')
def index():
    return render_template('inicio.html')

if __name__ == "__main__":
    app.run(debug=True, port=5030)