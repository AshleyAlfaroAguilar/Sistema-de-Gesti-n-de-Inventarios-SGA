from .db import get_connection

def validar_usuario(username, password):
    """
    Valida las credenciales del usuario.
    Devuelve un diccionario con los datos del usuario si son correctos,
    o None si no coinciden.
    """
    conn = get_connection()
    if not conn:
        print("No hay conexión a la base de datos.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdUsuario, Username, NombreCompleto, Rol, Activo
            FROM Usuarios
            WHERE Username = ? AND Password = ? AND Activo = 1
        """, (username, password))

        fila = cursor.fetchone()
        if fila:
            columnas = [col[0] for col in cursor.description]
            usuario = dict(zip(columnas, fila))
            return usuario
        else:
            return None

    except Exception as e:
        print("Error al validar usuario:", e)
        return None
    finally:
        conn.close()
