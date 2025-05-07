from models import db

class Convalidacion(db.Model):
    __tablename__ = 'convalidacion'
    id_convalidacion = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    detalle = db.Column(db.String(255))
    fecha = db.Column(db.Date, default=db.func.sysdate())

    def to_dict(self):
        return {
            'id_convalidacion': self.id_convalidacion,
            'id_estudiante': self.id_estudiante,
            'detalle': self.detalle,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
