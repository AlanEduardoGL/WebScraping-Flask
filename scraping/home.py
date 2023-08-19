from flask import (
    Blueprint, 
    render_template, 
    request
)
from .models import User
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint home
bp = Blueprint('home', __name__)


# @audit Route /
@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Function que muestra la página principal. 
    Obtiene todos los datos del webscraping
    por el usuario.

    Returns:
        render_template: Renderiza la plantilla index.html
    """
    
    
    return render_template('index.html')