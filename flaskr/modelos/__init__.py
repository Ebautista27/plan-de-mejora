# Importar la base de datos desde la inicialización principal de Flask
from flaskr import db

# Importar todos los modelos definidos en el archivo modelos.py
from flaskr.modelos.modelos import Usuario, Rol, Categoria, Servicio, Empleado, Cita

# Exponer los modelos para que estén disponibles al importar el paquete
__all__ = ['db', 'Usuario', 'Rol', 'Categoria', 'Servicio', 'Empleado', 'Cita']
