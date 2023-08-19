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


# @audit route /posts
@bp.route('/posts')
@login_required # ! Decorador para requerir la session en esta vista.
def posts():
    """
    Ruta/vista que muestra todos los resultados del WebScraping.

    Returns:
        render_template: Muestra la plantilla (admin/posts.html).
    """
    try:
        # posts = Post.query.all()
        posts = {
            'id_insumo': '1',
            'id_author_insumo': '1',
            'title_insumo': 'XBOX',
            'name_insumo': 'XBOX ONE SERIES S',
            'price_insumo': '6999',
            'attributes_insumo': 'XBOX ONE 1 TB ALMACENAMIENTO CARBON EDITION',
            'url_insumo': 'www.mercadolibre.com/xbox',
            'created': '2023-12-12'
        }
    except SQLAlchemyError as e:
        print(f'Error interno al mostrar resultados. Intenta nuevamente mas tarde. Mensaje: {str(e)}')
    else:
        return render_template('admin/posts.html', posts=posts)