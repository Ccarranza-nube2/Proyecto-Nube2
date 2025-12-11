import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 
from datetime import datetime

# Cargar las variables de entorno
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    tipo = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    precio = db.Column(db.Float, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)

# Crear las tablas
with app.app_context():
    db.create_all()

# Ruta principal - Lista de productos
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# Ruta para crear un nuevo producto 
@app.route('/producto/nuevo', methods=['GET'])
def nuevo_producto_form():
    return render_template('create_producto.html')

# Ruta para procesar la creación del producto
@app.route('/producto/nuevo', methods=['POST'])
def crear_producto():
    try:
        # Obtener datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        # Crear nuevo producto
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo,
            cantidad=cantidad,
            precio=precio
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        print(f"Producto '{nombre}' creado exitosamente")
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"Error al crear producto: {e}")
        db.session.rollback()
        return f"Error al crear producto: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)