from models import db
from datetime import datetime

class Matricula(db.Model):
    __tablename__ = 'matricula'
    id_matricula = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), nullable=False)
    fecha = db.Column(db.Date, default=db.func.sysdate())

    def to_dict(self):
        return {
            'id_matricula': self.id_matricula,
            'id_estudiante': self.id_estudiante,
            'id_curso': self.id_curso,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
