from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    g
)
from .auth import login_required
from .models import Post
from scraping import db
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint /post
bp = Blueprint('post', __name__, url_prefix='/post')


# @audit route /post
@bp.route('/post')
@login_required # ! Decorador para requerir la session en esta vista.
def posts():
    """
    Ruta/vista que muestra todos los resultados del WebScraping.

    Returns:
        render_template: Muestra la plantilla (admin/posts.html).
    """
    try:
        posts = Post.query.all()
    except SQLAlchemyError as e:
        print(f'Error interno al mostrar resultados. Intenta nuevamente mas tarde. Mensaje: {str(e)}')
    else:
        return render_template('admin/posts.html', posts=posts)