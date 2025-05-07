from flask import Blueprint, request
from flasgger import swag_from
from models.nota import Nota, db
from app_utils import custom_jsonify

nota_bp = Blueprint('nota_bp', __name__)

@nota_bp.route('/notas/count', methods=['GET'])
def count_notas():
    from models.nota import Nota
    count = Nota.query.count()
    return custom_jsonify({'count': count})

@nota_bp.route('/notas/top', methods=['GET'])
def top_notas():
    from models.nota import Nota
    from models.matricula import Matricula
    from models.estudiante import Estudiante
    from sqlalchemy import func
    top = (
        db.session.query(
            Estudiante.nombres,
            Estudiante.apellidos,
            func.count(Nota.id_nota).label('notas')
        )
        .join(Matricula, Nota.id_matricula == Matricula.id_matricula)
        .join(Estudiante, Matricula.id_estudiante == Estudiante.id_estudiante)
        .group_by(Estudiante.id_estudiante, Estudiante.nombres, Estudiante.apellidos)
        .order_by(func.count(Nota.id_nota).desc())
        .limit(5)
        .all()
    )
    return custom_jsonify([
        {'nombres': nombres, 'apellidos': apellidos, 'notas': notas} for nombres, apellidos, notas in top
    ])

    from models.nota import Nota
    count = Nota.query.count()
    return custom_jsonify({'count': count})

@nota_bp.route('/notas', methods=['POST'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Crear una nueva nota',
    'tags': ['Nota'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_matricula': {'type': 'integer', 'example': 1},
                    'nota': {'type': 'number', 'format': 'float', 'example': 18.5},
                    'observacion': {'type': 'string', 'example': 'Excelente'}
                },
                'required': ['id_matricula', 'nota']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Nota creada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_nota': {'type': 'integer', 'example': 1},
                    'id_matricula': {'type': 'integer', 'example': 1},
                    'nota': {'type': 'number', 'format': 'float', 'example': 18.5},
                    'observacion': {'type': 'string', 'example': 'Excelente'}
                }
            }
        }
    }
})
def crear_nota():
    data = request.json
    nota = Nota(
        id_matricula=data['id_matricula'],
        nota=data['nota'],
        observacion=data.get('observacion')
    )
    db.session.add(nota)
    db.session.commit()
    return custom_jsonify(nota, 201)

@nota_bp.route('/notas', methods=['GET'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Listar todas las notas',
    'description': 'Obtiene una lista de todas las notas registradas en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de notas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_nota': {'type': 'integer', 'example': 1},
                        'id_matricula': {'type': 'integer', 'example': 1},
                        'nota': {'type': 'number', 'format': 'float', 'example': 18.5},
                        'observacion': {'type': 'string', 'example': 'Excelente'}
                    }
                }
            }
        }
    }
})
def listar_notas():
    notas = Nota.query.all()
    return custom_jsonify([n.to_dict() for n in notas])

@nota_bp.route('/notas/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Obtener una nota por ID',
    'description': 'Devuelve la información de una nota específica según su ID.'
})
def obtener_nota(id):
    nota = Nota.query.get_or_404(id)
    return custom_jsonify(nota)

@nota_bp.route('/notas/buscar', methods=['GET'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Buscar notas',
    'description': 'Busca notas filtrando por matrícula.'
})
def buscar_nota():
    id_matricula = request.args.get('id_matricula')
    query = Nota.query
    if id_matricula:
        query = query.filter(Nota.id_matricula == id_matricula)
    notas = query.all()
    return custom_jsonify([n.to_dict() for n in notas])

@nota_bp.route('/notas/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Actualizar una nota',
    'description': 'Actualiza los datos de una nota existente.'
})
def actualizar_nota(id):
    data = request.json
    nota = Nota.query.get_or_404(id)
    nota.id_matricula = data.get('id_matricula', nota.id_matricula)
    nota.nota = data.get('nota', nota.nota)
    nota.observacion = data.get('observacion', nota.observacion)
    db.session.commit()
    return custom_jsonify(nota)

@nota_bp.route('/notas/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Eliminar una nota',
    'description': 'Elimina una nota por su ID.'
})
def eliminar_nota(id):
    nota = Nota.query.get_or_404(id)
    db.session.delete(nota)
    db.session.commit()
    return custom_jsonify({'message': 'Nota eliminada'})

@nota_bp.route('/notas/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Nota'],
    'summary': 'Restaurar una nota',
    'description': 'Restaura una nota previamente eliminada (si aplica).'
})
# Nota: No existe campo 'estado', así que esta función solo retorna un mensaje

def restaurar_nota(id):
    return custom_jsonify({'message': 'Función no implementada: no existe campo estado'})
