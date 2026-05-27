from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import hacer_login, hacer_logout

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        resultado = hacer_login(email, password)

        if resultado['exito']:
            datos_login = resultado['datos']

            session['token'] = datos_login['token']
            session['usuario_nombre'] = datos_login['datos']['nombre']
            session['usuario_rol'] = datos_login['datos']['rol']

            if datos_login['datos']['rol'] == 'alumno':
                return redirect(url_for('alumnos'))

            if datos_login['datos']['rol'] == 'docente':
                return redirect(url_for('docentes'))

        else:
            return render_template('auth/login.html', error=resultado['error'])

    return render_template('auth/login.html')
@auth_bp.route('/registro')
def registro():
    return render_template('auth/registro.html')

@auth_bp.route('/logout')
def logout():
    token_actual = session.get('token')

    if token_actual:
        hacer_logout(token_actual)

    session.clear()
    return redirect(url_for('index'))