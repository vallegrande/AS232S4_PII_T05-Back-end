from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config.from_pyfile('config/config.py')
db = SQLAlchemy(app)

with app.app_context():
    try:
        tablas = [
            'CURSO', 'ESTUDIANTE', 'MATRICULA', 'NOTA', 'CERTIFICADO', 'CONVALIDACION'
        ]
        for tabla in tablas:
            result = db.session.execute(text(f'SELECT COUNT(*) FROM {tabla}'))
            print(f"{tabla}: {result.scalar()}")
    except Exception as e:
        print("ERROR DE CONEXIÓN:", e)