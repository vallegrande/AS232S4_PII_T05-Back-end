from models import db

class Curso(db.Model):
    __tablename__ = 'curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_curso': self.id_curso,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
