from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database import SQLALCHEMY_DATABASE_URI
from sqlalchemy import text

app = Flask(__name__)
CORS(app)  # Permite peticiones desde React

# Configurar SQLAlchemy con Oracle Cloud
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Definir el modelo de la base de datos
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)  # Oracle lo maneja con trigger y secuencia
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas para obtener, crear, actualizar y eliminar productos
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify(producto.to_dict())
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/productos', methods=['POST'])
def create_producto():
    data = request.json
    nuevo_producto = Producto(
        nombre=data['nombre'],
        precio=data['precio']
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'id': nuevo_producto.id, 'nombre': nuevo_producto.nombre, 'precio': nuevo_producto.precio}), 201

@app.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    producto = Producto.query.get(id)
    if producto:
        producto.nombre = data['nombre']
        producto.precio = data['precio']
        db.session.commit()
        return jsonify(producto.to_dict())
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado'})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
