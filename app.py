from flask import Flask, render_template
from routes.auth import auth_bp
from routes.log import log_bp
from routes.asistencias import asistencias_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(log_bp, url_prefix='/log')
app.register_blueprint(asistencias_bp, url_prefix='/asistencias')

@app.route('/')
def index():
    return render_template('inicio.html')

if __name__ == "__main__":
    app.run(debug=True, port=5030)