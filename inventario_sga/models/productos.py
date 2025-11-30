from .db import get_connection

def obtener_todos_los_productos():
    """
    Devuelve una lista de diccionarios con todos los productos.
    """
    productos = []

    conn = get_connection()
    if not conn:
        return productos  # lista vacía si no hay conexión

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdProducto, Codigo, Nombre, Categoria,
                   Proveedor, PrecioCompra, PrecioVenta,
                   StockActual, StockMinimo, Activo, FechaCreacion
            FROM Productos
            ORDER BY Nombre
        """)

        columnas = [col[0] for col in cursor.description]

        for fila in cursor.fetchall():
            producto = dict(zip(columnas, fila))
            productos.append(producto)

    except Exception as e:
        print("Error al obtener productos:", e)
    finally:
        conn.close()

    return productos

def insertar_producto(codigo, nombre, categoria, proveedor,
                      precio_compra, precio_venta, stock):
    """
    Inserta un nuevo producto en la tabla Productos.
    """
    conn = get_connection()
    if not conn:
        print("No hay conexión a la base de datos.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Productos
                (Codigo, Nombre, Categoria, Proveedor,
                 PrecioCompra, PrecioVenta, StockActual, StockMinimo, Activo)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, 0, 1)
        """, (
            codigo,
            nombre,
            categoria,
            proveedor,
            float(precio_compra),
            float(precio_venta),
            int(stock)
        ))

        conn.commit()
        print("Producto insertado correctamente.")

    except Exception as e:
        print("Error al insertar producto:", e)
    finally:
        conn.close()


def obtener_producto_por_id(id_producto):
    """
    Devuelve un solo producto (diccionario) según su IdProducto.
    """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdProducto, Codigo, Nombre, Categoria,
                   Proveedor, PrecioCompra, PrecioVenta,
                   StockActual, StockMinimo, Activo, FechaCreacion
            FROM Productos
            WHERE IdProducto = ?
        """, (id_producto,))

        fila = cursor.fetchone()
        if fila:
            columnas = [col[0] for col in cursor.description]
            producto = dict(zip(columnas, fila))
            return producto
        else:
            return None

    except Exception as e:
        print("Error al obtener producto por id:", e)
        return None
    finally:
        conn.close()


def actualizar_producto(id_producto, codigo, nombre, categoria, proveedor,
                        precio_compra, precio_venta, stock):
    """
    Actualiza los datos de un producto existente.
    """
    conn = get_connection()
    if not conn:
        print("No hay conexión a la base de datos.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Productos
            SET Codigo = ?,
                Nombre = ?,
                Categoria = ?,
                Proveedor = ?,
                PrecioCompra = ?,
                PrecioVenta = ?,
                StockActual = ?
            WHERE IdProducto = ?
        """, (
            codigo,
            nombre,
            categoria,
            proveedor,
            float(precio_compra),
            float(precio_venta),
            int(stock),
            int(id_producto)
        ))

        conn.commit()
        print("Producto actualizado correctamente.")

    except Exception as e:
        print("Error al actualizar producto:", e)
    finally:
        conn.close()


def eliminar_producto(id_producto):
    """
    Elimina (o marca como inactivo) un producto por su IdProducto.
    """
    conn = get_connection()
    if not conn:
        print("No hay conexión a la base de datos.")
        return

    try:
        cursor = conn.cursor()

        # Borrado lógico 
        cursor.execute("""
            UPDATE Productos
            SET Activo = 0
            WHERE IdProducto = ?
        """, (int(id_producto),))

        conn.commit()
        print("Producto eliminado (marcado como inactivo).")

    except Exception as e:
        print("Error al eliminar producto:", e)
    finally:
        conn.close()

def obtener_productos_stock_bajo():
    """
    Devuelve una lista de productos cuyo StockActual es menor o igual al StockMinimo
    y que estén activos.
    """
    productos = []
    conn = get_connection()

    if not conn:
        print("No hay conexión a la base de datos.")
        return productos

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdProducto, Codigo, Nombre, Categoria, Proveedor,
                   PrecioCompra, PrecioVenta, StockActual, StockMinimo, Activo
            FROM Productos
            WHERE Activo = 1
              AND StockActual <= StockMinimo
            ORDER BY StockActual ASC
        """)

        columnas = [col[0] for col in cursor.description]

        for fila in cursor.fetchall():
            producto = dict(zip(columnas, fila))
            productos.append(producto)

    except Exception as e:
        print("Error al obtener productos con stock bajo:", e)
    finally:
        conn.close()

    return productos