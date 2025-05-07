from models import db
from datetime import datetime

class Certificado(db.Model):
    __tablename__ = 'certificado'
    id_certificado = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    fecha_emision = db.Column(db.Date, default=db.func.sysdate())
    descripcion = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_certificado': self.id_certificado,
            'id_estudiante': self.id_estudiante,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'descripcion': self.descripcion
        }
