from flask import Blueprint, request
from flasgger import swag_from
from models.certificado import Certificado, db
from app_utils import custom_jsonify

certificado_bp = Blueprint('certificado_bp', __name__)

@certificado_bp.route('/certificados/count', methods=['GET'])
def count_certificados():
    from models.certificado import Certificado
    count = Certificado.query.count()
    return custom_jsonify({'count': count})

@certificado_bp.route('/certificados/top', methods=['GET'])
def top_certificados():
    from models.certificado import Certificado
    from models.estudiante import Estudiante
    from sqlalchemy import func
    top = (
        db.session.query(
            Estudiante.nombres,
            Estudiante.apellidos,
            func.count(Certificado.id_certificado).label('certificados')
        )
        .join(Estudiante, Certificado.id_estudiante == Estudiante.id_estudiante)
        .group_by(Estudiante.id_estudiante, Estudiante.nombres, Estudiante.apellidos)
        .order_by(func.count(Certificado.id_certificado).desc())
        .limit(5)
        .all()
    )
    return custom_jsonify([
        {'nombres': nombres, 'apellidos': apellidos, 'certificados': certificados} for nombres, apellidos, certificados in top
    ])

    from models.certificado import Certificado
    count = Certificado.query.count()
    return custom_jsonify({'count': count})

@certificado_bp.route('/certificados', methods=['POST'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Crear un nuevo certificado',
    'tags': ['Certificado'],
    'summary': 'Crear un nuevo certificado',
    'description': 'Crea un nuevo certificado para un estudiante. Debes indicar el ID del estudiante, la fecha de emisión y una descripción.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                    'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                },
                'required': ['id_estudiante', 'fecha_emision']
            },
            'description': 'Datos del certificado a crear'
        }
    ],
    'responses': {
        201: {
            'description': 'Certificado creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_certificado': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                    'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                }
            }
        }
    }
})
def crear_certificado():
    data = request.json
    certificado = Certificado(
        id_estudiante=data['id_estudiante'],
        fecha_emision=data.get('fecha_emision'),
        descripcion=data.get('descripcion')
    )
    db.session.add(certificado)
    db.session.commit()
    return custom_jsonify(certificado, 201)

@certificado_bp.route('/certificados', methods=['GET'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Listar todos los certificados',
    'description': 'Obtiene una lista de todos los certificados registrados en la base de datos.',
    'responses': {
        200: {
            'description': 'Lista de certificados',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_certificado': {'type': 'integer', 'example': 1},
                        'id_estudiante': {'type': 'integer', 'example': 2},
                        'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                        'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                    }
                }
            }
        }
    }
})
def listar_certificados():
    certificados = Certificado.query.all()
    return custom_jsonify([c.to_dict() for c in certificados])

@certificado_bp.route('/certificados/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Obtener un certificado por ID',
    'description': 'Devuelve la información de un certificado específico según su ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del certificado a consultar'
        }
    ],
    'responses': {
        200: {
            'description': 'Certificado encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_certificado': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                    'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def obtener_certificado(id):
    certificado = Certificado.query.get_or_404(id)
    return custom_jsonify(certificado)

@certificado_bp.route('/certificados/buscar', methods=['GET'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Buscar certificados',
    'description': 'Busca certificados filtrando por ID de estudiante y/o descripción.',
    'parameters': [
        {
            'name': 'id_estudiante',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'ID del estudiante para filtrar'
        },
        {
            'name': 'descripcion',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Descripción del certificado para filtrar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de certificados filtrados',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_certificado': {'type': 'integer', 'example': 1},
                        'id_estudiante': {'type': 'integer', 'example': 1},
                        'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                        'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                    }
                }
            }
        }
    }
})
def buscar_certificado():
    id_estudiante = request.args.get('id_estudiante')
    descripcion = request.args.get('descripcion', '')
    query = Certificado.query
    if id_estudiante:
        query = query.filter(Certificado.id_estudiante == id_estudiante)
    if descripcion:
        query = query.filter(Certificado.descripcion.ilike(f"%{descripcion}%"))
    certificados = query.all()
    return custom_jsonify([c.to_dict() for c in certificados])

@certificado_bp.route('/certificados/<int:id>', methods=['PUT', 'PATCH'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Actualizar un certificado',
    'description': 'Actualiza los datos de un certificado existente.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del certificado a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                    'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                }
            },
            'description': 'Datos a actualizar'
        }
    ],
    'responses': {
        200: {
            'description': 'Certificado actualizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id_certificado': {'type': 'integer', 'example': 1},
                    'id_estudiante': {'type': 'integer', 'example': 1},
                    'fecha_emision': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                    'descripcion': {'type': 'string', 'example': 'Certificado de excelencia'}
                }
            }
        },
        404: {'description': 'No encontrado'}
    }
})
def actualizar_certificado(id):
    from datetime import datetime
    data = request.json
    certificado = Certificado.query.get_or_404(id)
    certificado.id_estudiante = data.get('id_estudiante', certificado.id_estudiante)
    fecha_emision_str = data.get('fecha_emision')
    if fecha_emision_str:
        try:
            certificado.fecha_emision = datetime.strptime(fecha_emision_str, "%Y-%m-%d").date()
        except ValueError:
            # Intenta con otro formato si es necesario
            certificado.fecha_emision = datetime.strptime(fecha_emision_str, "%d/%m/%Y").date()
    certificado.descripcion = data.get('descripcion', certificado.descripcion)
    db.session.commit()
    return custom_jsonify(certificado)

@certificado_bp.route('/certificados/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Eliminar un certificado',
    'description': 'Elimina un certificado específico por su ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del certificado a eliminar'
        }
    ],
    'responses': {
        200: {'description': 'Certificado eliminado'},
        404: {'description': 'No encontrado'}
    }
})
def eliminar_certificado(id):
    certificado = Certificado.query.get_or_404(id)
    db.session.delete(certificado)
    db.session.commit()
    return custom_jsonify({'message': 'Certificado eliminado'})

@certificado_bp.route('/certificados/<int:id>/restaurar', methods=['PUT'])
@swag_from({
    'tags': ['Certificado'],
    'summary': 'Restaurar un certificado',
    'description': 'Restaura un certificado previamente eliminado (si aplica).'
})
# Nota: No existe campo 'estado', así que esta función solo retorna un mensaje

def restaurar_certificado(id):
    return custom_jsonify({'message': 'Función no implementada: no existe campo estado'})
