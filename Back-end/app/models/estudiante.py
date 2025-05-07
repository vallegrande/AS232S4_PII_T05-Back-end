from models import db
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(15), unique=True, nullable=False)
    fecha_nac = db.Column(db.Date)
    direccion = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_estudiante': self.id_estudiante,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'dni': self.dni,
            'fecha_nac': self.fecha_nac.isoformat() if self.fecha_nac else None,
            'direccion': self.direccion
        }
