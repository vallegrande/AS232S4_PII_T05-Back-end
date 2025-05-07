from flask import Blueprint, request
from flasgger import swag_from
from models.convalidacion import Convalidacion, db
from app_utils import custom_jsonify

convalidacion_bp = Blueprint('convalidacion_bp', __name__)

@convalidacion_bp.route('/convalidaciones', methods=['POST'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Crear una nueva convalidación',
    'tags': ['Convalidacion'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'detalle': {'type': 'string', 'example': 'Convalidación parcial'},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                },
                'required': ['id_estudiante', 'detalle']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Convalidación creada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_convalidacion': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'detalle': {'type': 'string', 'example': 'Convalidación parcial'},
                    'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                }
            }
        }
    }
})
def crear_convalidacion():
    data = request.json
    convalidacion = Convalidacion(
        id_estudiante=data['id_estudiante'],
        detalle=data.get('detalle'),
        fecha=data.get('fecha')
    )
    db.session.add(convalidacion)
    db.session.commit()
    return custom_jsonify(convalidacion, 201)

@convalidacion_bp.route('/convalidaciones', methods=['GET'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Listar todas las convalidaciones',
    'description': 'Obtiene una lista de todas las convalidaciones registradas en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de convalidaciones',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_convalidacion': {'type': 'integer', 'example': 1},
                        'id_estudiante': {'type': 'integer', 'example': 1},
                        'detalle': {'type': 'string', 'example': 'Convalidación parcial'},
                        'fecha': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}
                    }
                }
            }
        }
    }
})
def listar_convalidaciones():
    convalidaciones = Convalidacion.query.all()
    return custom_jsonify([c.to_dict() for c in convalidaciones])

@convalidacion_bp.route('/convalidaciones/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Obtener una convalidación por ID',
    'description': 'Devuelve la información de una convalidación específica según su ID.'
})
def obtener_convalidacion(id):
    convalidacion = Convalidacion.query.get_or_404(id)
    return custom_jsonify(convalidacion)

@convalidacion_bp.route('/convalidaciones/buscar', methods=['GET'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Buscar convalidaciones',
    'description': 'Busca convalidaciones filtrando por estudiante.'
})
def buscar_convalidacion():
    id_estudiante = request.args.get('id_estudiante')
    query = Convalidacion.query
    if id_estudiante:
        query = query.filter(Convalidacion.id_estudiante == id_estudiante)
    convalidaciones = query.all()
    return custom_jsonify([c.to_dict() for c in convalidaciones])

@convalidacion_bp.route('/convalidaciones/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Actualizar una convalidación',
    'description': 'Actualiza los datos de una convalidación existente.'
})
def actualizar_convalidacion(id):
    data = request.json
    convalidacion = Convalidacion.query.get_or_404(id)
    convalidacion.id_estudiante = data.get('id_estudiante', convalidacion.id_estudiante)
    convalidacion.detalle = data.get('detalle', convalidacion.detalle)
    convalidacion.fecha = data.get('fecha', convalidacion.fecha)
    db.session.commit()
    return custom_jsonify(convalidacion)

@convalidacion_bp.route('/convalidaciones/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Eliminar una convalidación',
    'description': 'Elimina una convalidación por su ID.'
})
def eliminar_convalidacion(id):
    convalidacion = Convalidacion.query.get_or_404(id)
    convalidacion.estado = 'eliminado'
    db.session.commit()
    return custom_jsonify({'message': 'Convalidación eliminada (estado cambiado)'})

@convalidacion_bp.route('/convalidaciones/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Convalidacion'],
    'summary': 'Restaurar una convalidación',
    'description': 'Restaura una convalidación previamente eliminada (si aplica).'
})
def restaurar_convalidacion(id):
    convalidacion = Convalidacion.query.get_or_404(id)
    convalidacion.estado = 'activo'
    db.session.commit()
    return custom_jsonify({'message': 'Convalidación restaurada'})
