from flaskr import ma
from flaskr.modelos.modelos import Usuario, Rol, Categoria, Servicio, Empleado, Cita

# Esquema de Rol
class RolSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Rol
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()


# Esquema de Usuario
class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    email = ma.auto_field()
    rol = ma.Nested(RolSchema)  # Relación con Rol (serializa como objeto anidado)


# Esquema de Categoría
class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()


# Esquema de Servicio
class ServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Servicio
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()
    imagen = ma.auto_field()  # URL de la imagen en Cloudinary
    categoria = ma.Nested(CategoriaSchema)  # Relación con Categoría


# Esquema de Empleado
class EmpleadoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Empleado
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    imagen = ma.auto_field()  # URL de la imagen en Cloudinary


# Esquema de Cita
class CitaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cita
        load_instance = True

    id = ma.auto_field()
    fecha = ma.auto_field()
    hora = ma.auto_field()
    cliente = ma.Nested(UsuarioSchema)  # Relación con Usuario (cliente)
    empleado = ma.Nested(EmpleadoSchema)  # Relación con Empleado
    servicio = ma.Nested(ServicioSchema)  # Relación con Servicio
