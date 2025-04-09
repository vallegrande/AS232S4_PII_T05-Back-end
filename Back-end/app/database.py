import oracledb
import os
# Importar la librería dotenv para cargar variables de entorno
# de un archivo .env
# Asegúrate de tener instalada la librería dotenv
# Puedes instalarla usando pip:
# pip install python-dotenv

from dotenv import load_dotenv


# Cargar variables de entorno virtual desde un archivo .env
load_dotenv()
DB_USER = os.getenv("DB_USER", "SYSTEM")
DB_PASS = os.getenv("DB_PASS", "admin123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")
SQLALCHEMY_DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
# Conectar a Oracle XE en localhost # <-- Se corrigió la indentación

