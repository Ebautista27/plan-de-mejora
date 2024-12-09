from flaskr import create_app
from flaskr.modelos import db, Rol, Usuario
from werkzeug.security import generate_password_hash

def seed_roles():
    # Crear instancia de la aplicación
    app = create_app()
    with app.app_context():
        db.create_all()

        # Verificar si los roles ya están inicializados
        if not Rol.query.first():
            roles = [
                Rol(id=1, nombre="superadmin", descripcion="Usuario con acceso total."),
                Rol(id=2, nombre="cliente", descripcion="Cliente regular."),
                Rol(id=3, nombre="empleado", descripcion="Empleado de la peluquería.")
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()
            print("Roles inicializados correctamente.")
        else:
            print("Los roles ya están inicializados.")

        # Crear el superadmin si no existe
        if not Usuario.query.filter_by(email="superadmin@peluqueria.com").first():
            superadmin = Usuario(
                nombre="Super Admin",
                email="superadmin@peluqueria.com",
                contraseña=generate_password_hash("SuperPassword123"),  # Contraseña segura
                rol_id=1  # ID del rol de superadmin
            )
            db.session.add(superadmin)
            db.session.commit()
            print("Superadmin creado correctamente.")
        else:
            print("El superadmin ya existe.")

if __name__ == "__main__":
    seed_roles()
