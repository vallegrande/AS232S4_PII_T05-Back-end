from flask import Blueprint, request
from flasgger import swag_from
from models.estudiante import Estudiante, db
from app_utils import custom_jsonify

estudiante_bp = Blueprint('estudiante_bp', __name__)

@estudiante_bp.route('/estudiantes/count', methods=['GET'])
def count_estudiantes():
    from models.estudiante import Estudiante
    count = Estudiante.query.count()
    return custom_jsonify({'count': count})

@estudiante_bp.route('/estudiantes/top', methods=['GET'])
def top_estudiantes():
    from models.matricula import Matricula
    from models.estudiante import Estudiante
    from sqlalchemy import func
    top = (
        db.session.query(
            Estudiante.nombres,
            Estudiante.apellidos,
            func.count(Matricula.id_matricula).label('matriculas')
        )
        .join(Matricula, Matricula.id_estudiante == Estudiante.id_estudiante)
        .group_by(Estudiante.id_estudiante, Estudiante.nombres, Estudiante.apellidos)
        .order_by(func.count(Matricula.id_matricula).desc())
        .limit(5)
        .all()
    )
    return custom_jsonify([
        {'nombres': nombres, 'apellidos': apellidos, 'matriculas': matriculas} for nombres, apellidos, matriculas in top
    ])

    from models.estudiante import Estudiante
    count = Estudiante.query.count()
    return custom_jsonify({'count': count})

@estudiante_bp.route('/estudiantes', methods=['POST'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Crear un nuevo estudiante',
    'tags': ['Estudiante'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombres': {'type': 'string', 'example': 'Juan'},
                    'apellidos': {'type': 'string', 'example': 'Pérez'},
                    'dni': {'type': 'string', 'example': '12345678'},
                    'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                    'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                },
                'required': ['nombres', 'apellidos', 'dni']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Estudiante creado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'nombres': {'type': 'string', 'example': 'Juan'},
                    'apellidos': {'type': 'string', 'example': 'Pérez'},
                    'dni': {'type': 'string', 'example': '12345678'},
                    'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                    'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                }
            }
        }
    }
})
def crear_estudiante():
    data = request.json
    estudiante = Estudiante(
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        dni=data['dni'],
        fecha_nac=data.get('fecha_nac'),
        direccion=data.get('direccion')
    )
    db.session.add(estudiante)
    db.session.commit()
    return custom_jsonify(estudiante, 201)

@estudiante_bp.route('/estudiantes', methods=['GET'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Listar todos los estudiantes',
    'description': 'Obtiene una lista de todos los estudiantes registrados en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de estudiantes',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_estudiante': {'type': 'integer', 'example': 1},
                        'nombres': {'type': 'string', 'example': 'Juan'},
                        'apellidos': {'type': 'string', 'example': 'Pérez'},
                        'dni': {'type': 'string', 'example': '12345678'},
                        'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                        'direccion': {'type': 'string', 'example': 'Av. Siempre Viva 123'}
                    }
                }
            }
        }
    }
})
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return custom_jsonify([e.to_dict() for e in estudiantes])

@estudiante_bp.route('/estudiantes/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Obtener un estudiante por ID',
    'tags': ['Estudiante'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del estudiante'
        }
    ],
    'responses': {
        200: {
            'description': 'Estudiante encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'nombres': {'type': 'string', 'example': 'Juan'},
                    'apellidos': {'type': 'string', 'example': 'Pérez'},
                    'dni': {'type': 'string', 'example': '12345678'},
                    'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                    'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def obtener_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    return custom_jsonify(estudiante)

@estudiante_bp.route('/estudiantes/buscar', methods=['GET'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Buscar estudiantes',
    'tags': ['Estudiante'],
    'parameters': [
        {
            'name': 'nombres',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Nombres para filtrar'
        },
        {
            'name': 'apellidos',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Apellidos para filtrar'
        },
        {
            'name': 'dni',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'DNI para filtrar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de estudiantes filtrados',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_estudiante': {'type': 'integer', 'example': 1},
                        'nombres': {'type': 'string', 'example': 'Juan'},
                        'apellidos': {'type': 'string', 'example': 'Pérez'},
                        'dni': {'type': 'string', 'example': '12345678'},
                        'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                        'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                    }
                }
            }
        }
    }
})
def buscar_estudiante():
    nombres = request.args.get('nombres', '')
    apellidos = request.args.get('apellidos', '')
    dni = request.args.get('dni', '')
    query = Estudiante.query
    if nombres:
        query = query.filter(Estudiante.nombres.ilike(f"%{nombres}%"))
    if apellidos:
        query = query.filter(Estudiante.apellidos.ilike(f"%{apellidos}%"))
    if dni:
        query = query.filter(Estudiante.dni == dni)
    estudiantes = query.all()
    return custom_jsonify([e.to_dict() for e in estudiantes])

@estudiante_bp.route('/estudiantes/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Actualizar un estudiante',
    'tags': ['Estudiante'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del estudiante'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombres': {'type': 'string', 'example': 'Juan'},
                    'apellidos': {'type': 'string', 'example': 'Pérez'},
                    'dni': {'type': 'string', 'example': '12345678'},
                    'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                    'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Estudiante actualizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'nombres': {'type': 'string', 'example': 'Juan'},
                    'apellidos': {'type': 'string', 'example': 'Pérez'},
                    'dni': {'type': 'string', 'example': '12345678'},
                    'fecha_nac': {'type': 'string', 'format': 'date', 'example': '2000-01-01'},
                    'direccion': {'type': 'string', 'example': 'Calle Falsa 123'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def actualizar_estudiante(id):
    data = request.json
    estudiante = Estudiante.query.get_or_404(id)
    estudiante.nombres = data.get('nombres', estudiante.nombres)
    estudiante.apellidos = data.get('apellidos', estudiante.apellidos)
    estudiante.dni = data.get('dni', estudiante.dni)
    estudiante.fecha_nac = data.get('fecha_nac', estudiante.fecha_nac)
    estudiante.direccion = data.get('direccion', estudiante.direccion)
    db.session.commit()
    return custom_jsonify(estudiante)

@estudiante_bp.route('/estudiantes/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Eliminar un estudiante',
    'tags': ['Estudiante'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del estudiante'
        }
    ],
    'responses': {
        200: {'description': 'Estudiante eliminado'},
        404: {'description': 'No encontrado'}
    }
})
def eliminar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    db.session.delete(estudiante)
    db.session.commit()
    return custom_jsonify({'message': 'Estudiante eliminado'})

@estudiante_bp.route('/estudiantes/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Estudiante'],
    'summary': 'Restaurar un estudiante',
    'description': 'Restaura un estudiante previamente eliminado (si aplica).'
})
# Nota: No existe campo 'estado', así que esta función solo retorna un mensaje

def restaurar_estudiante(id):
    return custom_jsonify({'message': 'Función no implementada: no existe campo estado'})
