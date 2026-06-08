from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import hacer_login, hacer_logout, registrar_nuevo_usuario

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
            session['email'] = datos_login['datos']['email']
            session['usuario_nombre'] = datos_login['datos']['nombre']
            session['usuario_rol'] = datos_login['datos']['rol']

            if datos_login['datos']['rol'] == 'alumno':
                return redirect(url_for('index'))

            if datos_login['datos']['rol'] == 'docente':
                return redirect(url_for('index'))

        else:
            return render_template('auth/login.html', error=resultado['error'])

    return render_template('auth/login.html')
@auth_bp.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        password = request.form.get('password')
        padron = request.form.get('padron')

        resultado = registrar_nuevo_usuario(nombre, apellido, password, email, padron)

        if resultado['exito'] == True:
            flash(f"¡Cuenta creada con éxito! Iniciá sesión para continuar.", "success")
            return redirect(url_for('auth.registro'))

        else:
            return render_template('auth/registro.html', error=resultado['error'])

    return render_template('auth/registro.html')

@auth_bp.route('/logout')
def logout():
    token_actual = session.get('token')

    if token_actual:
        hacer_logout(token_actual)

    session.clear()
    flash("Has cerrado sesión correctamente. ¡Hasta pronto!", "info")
    return redirect(url_for('index'))