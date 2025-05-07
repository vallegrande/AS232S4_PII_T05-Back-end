from flask import Blueprint, request
from flasgger import swag_from
from models.matricula import Matricula, db
from app_utils import custom_jsonify

matricula_bp = Blueprint('matricula_bp', __name__)

@matricula_bp.route('/matriculas/count', methods=['GET'])
def count_matriculas():
    from models.matricula import Matricula
    count = Matricula.query.count()
    return custom_jsonify({'count': count})

@matricula_bp.route('/matriculas/top', methods=['GET'])
def top_matriculas():
    from models.matricula import Matricula
    from models.curso import Curso
    from sqlalchemy import func
    top = (
        db.session.query(
            Curso.nombre,
            func.count(Matricula.id_matricula).label('matriculas')
        )
        .join(Curso, Matricula.id_curso == Curso.id_curso)
        .group_by(Curso.id_curso, Curso.nombre)
        .order_by(func.count(Matricula.id_matricula).desc())
        .limit(5)
        .all()
    )
    return custom_jsonify([
        {'nombre': nombre, 'matriculas': matriculas} for nombre, matriculas in top
    ])

    from models.matricula import Matricula
    count = Matricula.query.count()
    return custom_jsonify({'count': count})

@matricula_bp.route('/matriculas', methods=['POST'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Crear una nueva matrícula',
    'tags': ['Matricula'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'id_curso': {'type': 'integer', 'example': 2},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                },
                'required': ['id_estudiante', 'id_curso']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Matrícula creada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_matricula': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'id_curso': {'type': 'integer', 'example': 2},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                }
            }
        }
    }
})
def crear_matricula():
    data = request.json
    matricula = Matricula(
        id_estudiante=data['id_estudiante'],
        id_curso=data['id_curso'],
        fecha=data.get('fecha')
    )
    db.session.add(matricula)
    db.session.commit()
    return custom_jsonify(matricula, 201)

@matricula_bp.route('/matriculas', methods=['GET'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Listar todas las matrículas',
    'description': 'Obtiene una lista de todas las matrículas registradas en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de matrículas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_matricula': {'type': 'integer', 'example': 1},
                        'id_estudiante': {'type': 'integer', 'example': 1},
                        'id_curso': {'type': 'integer', 'example': 1},
                        'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                    }
                }
            }
        }
    }
})
def listar_matriculas():
    id_estudiante = request.args.get('id_estudiante', type=int)
    id_curso = request.args.get('id_curso', type=int)
    matriculas = Matricula.query.all()
    if id_estudiante:
        matriculas = [m for m in matriculas if m.id_estudiante == id_estudiante]
    if id_curso:
        matriculas = [m for m in matriculas if m.id_curso == id_curso]
    return custom_jsonify([m.to_dict() for m in matriculas])

@matricula_bp.route('/matriculas/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Obtener una matrícula por ID',
    'tags': ['Matricula'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la matrícula'
        }
    ],
    'responses': {
        200: {
            'description': 'Matrícula encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_matricula': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'id_curso': {'type': 'integer', 'example': 2},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                }
            }
        },
        404: {'description': 'No encontrada'}
    }
})
def obtener_matricula(id):
    matricula = Matricula.query.get_or_404(id)
    return custom_jsonify(matricula)

@matricula_bp.route('/matriculas/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Actualizar una matrícula',
    'tags': ['Matricula'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la matrícula'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'id_curso': {'type': 'integer', 'example': 2},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Matrícula actualizada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_matricula': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'id_curso': {'type': 'integer', 'example': 2},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                }
            }
        },
        404: {'description': 'No encontrada'}
    }
})
def actualizar_matricula(id):
    data = request.json
    matricula = Matricula.query.get_or_404(id)
    matricula.id_estudiante = data.get('id_estudiante', matricula.id_estudiante)
    matricula.id_curso = data.get('id_curso', matricula.id_curso)
    matricula.fecha = data.get('fecha', matricula.fecha)
    db.session.commit()
    return custom_jsonify(matricula)

@matricula_bp.route('/matriculas/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Eliminar una matrícula',
    'tags': ['Matricula'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la matrícula'
        }
    ],
    'responses': {
        200: {'description': 'Matrícula eliminada'},
        404: {'description': 'No encontrada'}
    }
})
def eliminar_matricula(id):
    matricula = Matricula.query.get_or_404(id)
    db.session.delete(matricula)
    db.session.commit()
    return custom_jsonify({'message': 'Matrícula eliminada'})

@matricula_bp.route('/matriculas/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Matricula'],
    'summary': 'Restaurar una matrícula',
    'description': 'Restaura una matrícula previamente eliminada (si aplica).'
})
# Nota: No existe campo 'estado', así que esta función solo retorna un mensaje

def restaurar_matricula(id):
    return custom_jsonify({'message': 'Función no implementada: no existe campo estado'})
