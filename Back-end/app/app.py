from flask import Flask
from models import db
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config.from_pyfile('config/config.py')

CORS(app)
swagger = Swagger(app)
db.init_app(app)

# Importa y registra los Blueprints de cada entidad
from routes.estudiante import estudiante_bp
from routes.matricula import matricula_bp
from routes.curso import curso_bp
from routes.nota import nota_bp
from routes.certificado import certificado_bp
from routes.convalidacion import convalidacion_bp

app.register_blueprint(estudiante_bp)
app.register_blueprint(matricula_bp)
app.register_blueprint(curso_bp)
app.register_blueprint(nota_bp)
app.register_blueprint(certificado_bp)
app.register_blueprint(convalidacion_bp)

if __name__ == '__main__':
    app.run(debug=True)