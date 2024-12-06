from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # Para solicitudes de otros dominios
import cloudinary

# Configuración de Cloudinary
cloudinary.config(
    cloud_name='estif',
    api_key='826745631121761',
    api_secret='9UMa7cqyphQZ3wA7moTj1gnjVF8'
)

# Inicializar extensiones
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/peluqueria'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'

    # Inicializar extensiones con la app
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registrar rutas con Flask-Restful
    from flask_restful import Api
    from flaskr.vistas.vistas import (
        VistaInicio, VistaRegistro, VistaLogin,
        VistaCrearCategoria, VistaListarCategorias,
        VistaCrearServicio, VistaSubirImagenServicio, VistaVerServicio,
        VistaActualizarServicio, VistaEliminarServicio,
        VistaAgendarCita, VistaConsultarDisponibilidad
    )

    api = Api(app)

    # ==================== Registro de Rutas ==================== #
    # Rutas de autenticación
    api.add_resource(VistaInicio, '/')
    api.add_resource(VistaRegistro, '/registro')
    api.add_resource(VistaLogin, '/login')

    # Rutas de categorías y servicios
    api.add_resource(VistaCrearCategoria, '/categorias')
    api.add_resource(VistaListarCategorias, '/categorias/listar')
    api.add_resource(VistaCrearServicio, '/servicios')
    api.add_resource(VistaSubirImagenServicio, '/servicios/<int:servicio_id>/imagen')

    # Nuevas rutas para servicios
    api.add_resource(VistaVerServicio, '/servicios/<int:servicio_id>')
    api.add_resource(VistaActualizarServicio, '/servicios/<int:servicio_id>/actualizar')
    api.add_resource(VistaEliminarServicio, '/servicios/<int:servicio_id>/eliminar')

    # Rutas de citas
    api.add_resource(VistaAgendarCita, '/citas')
    api.add_resource(VistaConsultarDisponibilidad, '/disponibilidad/<int:empleado_id>')

    return app
