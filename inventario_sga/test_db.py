from models.db import get_connection

conn = get_connection()

if conn:
    print("Conexión exitosa con SQL Server")
else:
    print("No se pudo conectar")
