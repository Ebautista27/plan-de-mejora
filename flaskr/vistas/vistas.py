from flask_restful import Resource
from flask import request, jsonify
from flaskr import db
from flaskr.modelos.modelos import Usuario, Rol, Categoria, Servicio, Cita
from flaskr.modelos.esquemas import UsuarioSchema, CategoriaSchema, ServicioSchema, CitaSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
import cloudinary.uploader

# Esquemas para serialización
usuario_schema = UsuarioSchema()
categoria_schema = CategoriaSchema()
servicio_schema = ServicioSchema()
cita_schema = CitaSchema()

# ==================== Vistas ==================== #

class VistaInicio(Resource):
    def get(self):
        return {"mensaje": "Bienvenido a la API de la Peluquería"}, 200


class VistaRegistro(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"error": "Datos no proporcionados"}, 400

        nombre = data.get('nombre')
        email = data.get('email')
        contraseña = generate_password_hash(data.get('contraseña'))
        rol = Rol.query.filter_by(nombre='cliente').first()

        if Usuario.query.filter_by(email=email).first():
            return {"error": "El email ya está registrado"}, 400

        nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return usuario_schema.dump(nuevo_usuario), 201


class VistaLogin(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        contraseña = data.get('contraseña')

        print("Email recibido:", email)
        print("Contraseña recibida:", contraseña)

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            print("Usuario no encontrado")
            return {"error": "Credenciales inválidas"}, 401

        if not check_password_hash(usuario.contraseña, contraseña):
            print("Contraseña inválida")
            return {"error": "Credenciales inválidas"}, 401

        token = create_access_token(identity={"id": usuario.id, "rol": usuario.rol.nombre})
        return {"access_token": token}, 200


class VistaCrearCategoria(Resource):
    def post(self):
        data = request.json
        nueva_categoria = Categoria(
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria), 201


class VistaListarCategorias(Resource):
    def get(self):
        categorias = Categoria.query.all()
        return categoria_schema.dump(categorias, many=True), 200


class VistaCrearServicio(Resource):
    def post(self):
        data = request.json
        nueva_servicio = Servicio(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria_id=data['categoria_id']
        )
        db.session.add(nueva_servicio)
        db.session.commit()
        return servicio_schema.dump(nueva_servicio), 201


class VistaSubirImagenServicio(Resource):
    def post(self, servicio_id):
        servicio = Servicio.query.get_or_404(servicio_id)
        imagen = request.files.get('imagen')
        if not imagen:
            return {"error": "No se ha proporcionado una imagen"}, 400

        # Subir a Cloudinary
        upload_result = cloudinary.uploader.upload(imagen)
        servicio.imagen = upload_result.get("url")
        db.session.commit()
        return servicio_schema.dump(servicio), 200


class VistaVerServicio(Resource):
    def get(self, servicio_id):
        servicio = Servicio.query.get_or_404(servicio_id)
        return servicio_schema.dump(servicio), 200


class VistaActualizarServicio(Resource):
    @jwt_required()
    def put(self, servicio_id):
        servicio = Servicio.query.get_or_404(servicio_id)
        data = request.json
        servicio.nombre = data.get('nombre', servicio.nombre)
        servicio.descripcion = data.get('descripcion', servicio.descripcion)
        servicio.categoria_id = data.get('categoria_id', servicio.categoria_id)
        db.session.commit()
        return servicio_schema.dump(servicio), 200



class VistaEliminarServicio(Resource):
    @jwt_required()
    def delete(self, servicio_id):
        servicio = Servicio.query.get_or_404(servicio_id)
        db.session.delete(servicio)
        db.session.commit()
        return '', 204


class VistaAgendarCita(Resource):
    def post(self):
        data = request.json
        nueva_cita = Cita(
            fecha=data['fecha'],
            hora=data['hora'],
            cliente_id=data['cliente_id'],
            empleado_id=data['empleado_id'],
            servicio_id=data['servicio_id']
        )
        db.session.add(nueva_cita)
        db.session.commit()
        return cita_schema.dump(nueva_cita), 201


class VistaConsultarDisponibilidad(Resource):
    def get(self, empleado_id):
        citas = Cita.query.filter_by(empleado_id=empleado_id).all()
        horarios_ocupados = [{"fecha": c.fecha, "hora": c.hora} for c in citas]
        return horarios_ocupados, 200
