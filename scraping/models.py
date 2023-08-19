from scraping import db
from datetime import datetime


# @audit Tbl Users
class User(db.Model):
    # Colocamos nombre tabla.
    __tablename__ = "users"
    
    # Colocamos columnas tabla.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(260))
    
    # Metodo Constructor.
    def __init__(self, username, email, password, photo=None):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo
        
    # Funcion para mostrar cada elemento en el shell.
    def __repr__(self):
        return f'User: "{self.username}", Email: "{self.email}"'
    

# @audit Tbl Post
class Post(db.Model):
    # Colocamos nombre tabla.
    __tablename__ = "posts"

    # Colocamos columnas tablas.
    id_insumo = db.Column(db.Integer, primary_key=True)
    id_author_insumo = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title_insumo = db.Column(db.String(100), unique=False, nullable=False)
    name_insumo = db.Column(db.String(100), nullable=False)
    price_insumo = db.Column(db.Float, nullable=False)
    attributes_insumo = db.Column(db.String(1000), unique=False, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Creamos el Metodo Constructor
    def __init__(self, id_author_insumo, title_insumo, name_insumo, price_insumo, attributes_insumo, url) -> None:
        self.id_author_insumo = id_author_insumo        
        self.title_insumo = title_insumo        
        self.name_insumo = name_insumo        
        self.price_insumo = price_insumo        
        self.attributes_insumo = attributes_insumo        
        self.url = url        

    # Colocamos como vamos a representar cada uno de estos elementos en el Shell.
    def __repr__(self) -> str:
        return f"Post: {self.title_insumo}"