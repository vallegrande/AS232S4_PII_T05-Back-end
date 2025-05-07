import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Variables de entorno con valores predeterminados
DB_USER = os.getenv("DB_USER", "system")
DB_PASS = os.getenv("DB_PASS", "12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "XE")  

# Configurar NLS_LANG para Oracle
os.environ['NLS_LANG'] = '.AL32UTF8'

# URI para SQLAlchemy (usando oracledb)
SQLALCHEMY_DATABASE_URI = (
    f"oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False