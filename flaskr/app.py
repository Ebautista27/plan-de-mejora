from flaskr import create_app
from flaskr.modelos import db, Rol

# Crear la instancia de la aplicación Flask
app = create_app()

# Función para inicializar roles
def seed_roles():
    with app.app_context():
        db.create_all()

        # Verificar si ya existen roles para evitar duplicados
        if not Rol.query.first():
            roles = [
                Rol(nombre="superadmin", descripcion="Usuario con acceso total."),
                Rol(nombre="cliente", descripcion="Cliente regular."),
                Rol(nombre="empleado", descripcion="Empleado de la peluquería."),
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()
            print("Roles inicializados correctamente.")
        else:
            print("Los roles ya están inicializados.")

# Ejecutar la aplicación
if __name__ == '__main__':
    seed_roles()
    app.run(debug=True, host='0.0.0.0', port=5000)



