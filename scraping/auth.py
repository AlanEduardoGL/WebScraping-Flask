import functools
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from .models import User
from scraping import db
# Elimina espacios de una imagen y agrega barra baja.
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')


# @audit Route /auth
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta/vista que registra un nuevo usuario.
    Recibe metodos 'GET' y 'POST'.

    Returns:
        redirect: (auth.login) Nos redirige al login.
        error: Se mostrará un mensaje de error si existe el usuario.
    """
    if request.method == 'POST':
        try:
            # Recuperamos datos del formulario.
            username = request.form.get('username')
            email = request.form.get('email')
            confirm_email = request.form.get('confirm_email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            message = None

            # Validamos que email y password sean similares.
            if email == confirm_email and password == confirm_password:
                # Revisamos que no exista la cuenta.
                user_email = User.query.filter_by(email=email).first()

                # Validamos existencia.
                if user_email == None:
                    try:
                        # Creamos objeto con los datos obtenidos.
                        user = User(
                            username,
                            email,
                            generate_password_hash(password)
                        )

                        # Agregamos usuario nuevo.
                        db.session.add(user)
                        # Confirmamos los cambios en la base de datos.
                        db.session.commit()
                    except SQLAlchemyError as e:
                        message = f'Error interno al registrar el usuario "{username}". Mensaje: {str(e)}.'
                    else:
                        return redirect(url_for('auth.login'))
                else:
                    message = f'El correo electrónico "{email}" ya se encuentra registrado.'
            else:
                message = f'El correo electrónico y/o contraseña no son similares. Valida tu información.'
                
            # Enviamos mensajes de alerta en caso de existencia.
            flash(message)
        except SQLAlchemyError as e:
            message = f"¡Error interno!. Intentalo mas tarde. Mensaje: {str(e)}"           

    return render_template('auth/register.html')


# @audit Route /login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta/vista para iniciar sesión del usuario.
    Recibe methods 'GET' y 'POST'.

    Returns:
        redirect: (post.posts) Nos redirige a nuestros posts publicados.
        error: Se mostrará un mensaje de error si no coinciden las credenciales.
    """
    if request.method == 'POST':
        try:
            # Recuperamos datos del formulario.
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Recuperemos el usuario registrado.
            user = User.query.filter_by(email=email).first()
            
            message = None
            
            # Validamos los datos ingresados por el usuario para iniciar sesión.
            if user is None or not check_password_hash(user.password, password):
                message = f'El correo electrónico y/o contraseña son incorrectos. Intenta nuevamente.'
            else:
                if message == None:
                    # Limpiamos cualquier sesión iniciada.
                    session.clear()
                    # Obtenemos id del usuario.
                    session['user_id'] = user.id
                    
                    return redirect(url_for('home.index'))
                
            # Enviamos mensajes de alerta en caso de existencia.
            flash(message)
        except SQLAlchemyError as e:
            message = f'Ocurrio un error al iniciar sesión. Intentalo mas tarde. Mensaje: {str(e)}.'            
    
    return render_template('auth/login.html')


# @audit Function load_logged_in_user()
@bp.before_app_request
def load_logged_in_user():
    """ 
    Mantiene la session del usuario activa.
    Se ejecuta antes de cada solicitud entrante a la aplicación 
    (antes de que se maneje una vista).

    Returns:
        g.user: Alamcena todos los datos del usuario 
        activo en la session.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = User.query.get(user_id)
        except SQLAlchemyError as e:
            print(
                f'No existe usuario registrado con id "{user_id}". Mensaje: {str(e)}.')
            
            
# @audit Route /logout
@bp.route('/logout')
def logout():
    """
    Ruta/vista para cerrar session del usuario.

    Returns:
        redirect: Nos redirije al index principal.
    """
    try:
        session.clear()
    except SQLAlchemyError as e:
        print(
            f'Error interno al cerrar sesión. Intenta nuevamente. Mensaje: {str(e)}')
    else:
        return redirect(url_for('home.index'))
    
    
# @audit Function login_required()
def login_required(view):
    """
    Asegura que el usuario haya iniciado session
    antes de que pueda acceder a una vista o ruta específica.

    Args:
        view (vista): La vista representa la función que se asocia con 
        una ruta específica en la aplicación.

    Returns:
        redirect: (auth.login) Si el usuario no ha iniciado sesión, 
        se redirige automáticamente a la página de inicio.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)

    return wrapped_view