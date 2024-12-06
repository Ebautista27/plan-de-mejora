from flaskr import db  # Base de datos SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Time  # Para columnas y relaciones
from sqlalchemy.orm import relationship  # Para definir relaciones en los modelos
from werkzeug.security import generate_password_hash, check_password_hash  # Para manejo de contraseñas (opcional)


# Modelo de Rol
class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)  # Ej: cliente, admin, superadmin
    descripcion = db.Column(db.String(100), nullable=True)  # Descripción opcional del rol

    # Relación con Usuarios
    usuarios = db.relationship('Usuario', back_populates='rol')


# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

    # Relación con Rol
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    rol = db.relationship('Rol', back_populates='usuarios')

    # Relación con las citas
    citas = db.relationship('Cita', back_populates='cliente')


# Modelo de Categoria
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)

    # Relación con los servicios
    servicios = db.relationship('Servicio', back_populates='categoria')


# Modelo de Servicio
class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(255))  # URL de la imagen en Cloudinary

    # Relación con Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='servicios')

    # Relación con las citas
    citas = db.relationship('Cita', back_populates='servicio')


# Modelo de Empleado
class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(255))  # Foto del empleado en Cloudinary

    # Relación con las citas
    citas = db.relationship('Cita', back_populates='empleado')


# Modelo de Cita
class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    # Relaciones con otras tablas
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)

    cliente = db.relationship('Usuario', back_populates='citas')
    empleado = db.relationship('Empleado', back_populates='citas')
    servicio = db.relationship('Servicio', back_populates='citas')
