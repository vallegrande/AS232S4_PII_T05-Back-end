from flask import Blueprint, request
from flasgger import swag_from
from models.curso import Curso, db
from app_utils import custom_jsonify

curso_bp = Blueprint('curso_bp', __name__)

@curso_bp.route('/cursos/count', methods=['GET'])
def count_cursos():
    count = Curso.query.count()
    return custom_jsonify({'count': count})

@curso_bp.route('/cursos/top', methods=['GET'])
def top_cursos():
    from models.matricula import Matricula
    from sqlalchemy import func
    top = db.session.query(
        Curso.nombre,
        func.count(Matricula.id_matricula).label('matriculas')
    ).join(Matricula, Matricula.id_curso == Curso.id_curso)
    top = top.group_by(Curso.id_curso, Curso.nombre).order_by(func.count(Matricula.id_matricula).desc()).limit(5).all()
    return custom_jsonify([
        {'nombre': nombre, 'matriculas': matriculas} for nombre, matriculas in top
    ])

@curso_bp.route('/cursos', methods=['POST'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Crear un nuevo curso',
    'tags': ['Curso'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Matemática'},
                    'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                },
                'required': ['nombre']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Curso creado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_curso': {'type': 'integer', 'example': 1},
                    'nombre': {'type': 'string', 'example': 'Matemática'},
                    'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                }
            }
        }
    }
})
def crear_curso():
    data = request.json
    curso = Curso(
        nombre=data['nombre'],
        descripcion=data.get('descripcion')
    )
    db.session.add(curso)
    db.session.commit()
    return custom_jsonify(curso, 201)

@curso_bp.route('/cursos', methods=['GET'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Listar todos los cursos',
    'description': 'Obtiene una lista de todos los cursos registrados en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de cursos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_curso': {'type': 'integer', 'example': 1},
                        'nombre': {'type': 'string', 'example': 'Matemática'},
                        'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                    }
                }
            }
        }
    }
})
def listar_cursos():
    cursos = Curso.query.all()
    return custom_jsonify([c.to_dict() for c in cursos])

@curso_bp.route('/cursos/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Obtener un curso por ID',
    'tags': ['Curso'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        }
    ],
    'responses': {
        200: {
            'description': 'Curso encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_curso': {'type': 'integer', 'example': 1},
                    'nombre': {'type': 'string', 'example': 'Matemática'},
                    'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def obtener_curso(id):
    curso = Curso.query.get_or_404(id)
    return custom_jsonify(curso)

@curso_bp.route('/cursos/buscar', methods=['GET'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Buscar cursos',
    'tags': ['Curso'],
    'parameters': [
        {
            'name': 'nombre',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Nombre del curso para filtrar'
        },
        {
            'name': 'descripcion',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Descripción para filtrar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de cursos filtrados',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_curso': {'type': 'integer', 'example': 1},
                        'nombre': {'type': 'string', 'example': 'Matemática'},
                        'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                    }
                }
            }
        }
    }
})
def buscar_curso():
    nombre = request.args.get('nombre', '')
    descripcion = request.args.get('descripcion', '')
    query = Curso.query
    if nombre:
        query = query.filter(Curso.nombre.ilike(f"%{nombre}%"))
    if descripcion:
        query = query.filter(Curso.descripcion.ilike(f"%{descripcion}%"))
    cursos = query.all()
    return custom_jsonify([c.to_dict() for c in cursos])

@curso_bp.route('/cursos/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Actualizar un curso',
    'tags': ['Curso'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Matemática'},
                    'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Curso actualizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_curso': {'type': 'integer', 'example': 1},
                    'nombre': {'type': 'string', 'example': 'Matemática'},
                    'descripcion': {'type': 'string', 'example': 'Curso de matemáticas básicas'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def actualizar_curso(id):
    data = request.json
    curso = Curso.query.get_or_404(id)
    curso.nombre = data.get('nombre', curso.nombre)
    curso.descripcion = data.get('descripcion', curso.descripcion)
    db.session.commit()
    return custom_jsonify(curso)

@curso_bp.route('/cursos/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Eliminar un curso',
    'tags': ['Curso'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del curso'
        }
    ],
    'responses': {
        200: {'description': 'Curso eliminado'},
        404: {'description': 'No encontrado'}
    }
})
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return custom_jsonify({'message': 'Curso eliminado'})

@curso_bp.route('/cursos/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Curso'],
    'summary': 'Restaurar un curso',
    'description': 'Restaura un curso previamente eliminado (si aplica).'
})
# Nota: No existe campo 'estado', así que esta función solo retorna un mensaje

def restaurar_curso(id):
    return custom_jsonify({'message': 'Función no implementada: no existe campo estado'})
