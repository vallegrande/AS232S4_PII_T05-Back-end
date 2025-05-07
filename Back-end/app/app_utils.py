#Evita errores de importaciones
from flask import jsonify

def custom_jsonify(data, status_code=200):
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    elif isinstance(data, list) and len(data) > 0 and hasattr(data[0], 'to_dict'):
        data = [item.to_dict() for item in data]
    response = jsonify(data)
    response.status_code = status_code
    return response
