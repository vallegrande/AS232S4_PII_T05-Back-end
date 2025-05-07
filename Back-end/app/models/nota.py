from models import db

class Nota(db.Model):
    __tablename__ = 'nota'
    id_nota = db.Column(db.Integer, primary_key=True)
    id_matricula = db.Column(db.Integer, db.ForeignKey('matricula.id_matricula'), nullable=False)
    nota = db.Column(db.Numeric(5,2), nullable=False)
    observacion = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_nota': self.id_nota,
            'id_matricula': self.id_matricula,
            'nota': float(self.nota),
            'observacion': self.observacion
        }
