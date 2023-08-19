"""
Archivo que contiene la configuración del proyecto.
"""


SQLITE = "sqlite:///web_scraping.db"

# ! CONFIGURACIÓN PARA POSTGRESQL !
# ! Cambiar el Port si es Windows o Macbook !
# ! Windows Port: 5432 "Versión PostgreSQL 15" !
# ! Macbook Port: 5433 "Versión PostgreSQL 11" !
POSTGRESQL = "postgresql+psycopg2://postgres:root@localhost:5432/web_scraping_db"


# @audit Class Config
class Config():
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = SQLITE
