from .db import get_connection

def registrar_movimiento(id_producto, tipo_movimiento, cantidad,
                         referencia=None, observaciones=None):
    """
    Registra un movimiento de inventario (ENTRADA o SALIDA) y actualiza el stock del producto.
    """

    conn = get_connection()
    if not conn:
        print("No hay conexión a la base de datos.")
        return False

    try:
        cursor = conn.cursor()

        # 1. Obtener stock actual del producto
        cursor.execute("""
            SELECT StockActual
            FROM Productos
            WHERE IdProducto = ?
        """, (int(id_producto),))

        fila = cursor.fetchone()
        if not fila:
            print("Producto no encontrado.")
            return False

        stock_anterior = fila[0]
        cantidad = int(cantidad)

        # 2. Calcular stock nuevo según el tipo de movimiento
        if tipo_movimiento.upper() == "ENTRADA":
            stock_nuevo = stock_anterior + cantidad
        elif tipo_movimiento.upper() == "SALIDA":
            stock_nuevo = stock_anterior - cantidad
            if stock_nuevo < 0:
                print("No hay suficiente stock para la salida.")
                return False
        else:
            print("Tipo de movimiento no válido. Use ENTRADA o SALIDA.")
            return False

        # 3. Insertar el movimiento en la tabla MovimientosInventario
        cursor.execute("""
            INSERT INTO MovimientosInventario
                (IdProducto, TipoMovimiento, Cantidad,
                 Referencia, Observaciones,
                 StockAnterior, StockNuevo)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (
            int(id_producto),
            tipo_movimiento.upper(),
            cantidad,
            referencia,
            observaciones,
            stock_anterior,
            stock_nuevo
        ))

        # 4. Actualizar el stock del producto
        cursor.execute("""
            UPDATE Productos
            SET StockActual = ?
            WHERE IdProducto = ?
        """, (stock_nuevo, int(id_producto)))

        conn.commit()
        print("Movimiento registrado correctamente.")
        return True

    except Exception as e:
        print("Error al registrar movimiento:", e)
        return False
    finally:
        conn.close()


def obtener_movimientos_por_producto(id_producto):
    """
    Devuelve una lista de movimientos de inventario para un producto específico.
    """
    conn = get_connection()
    movimientos = []

    if not conn:
        print("No hay conexión a la base de datos.")
        return movimientos

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                m.IdMovimiento,
                m.TipoMovimiento,
                m.Cantidad,
                m.FechaMovimiento,
                m.Referencia,
                m.Observaciones,
                m.StockAnterior,
                m.StockNuevo,
                p.Codigo,
                p.Nombre
            FROM MovimientosInventario m
            INNER JOIN Productos p ON m.IdProducto = p.IdProducto
            WHERE m.IdProducto = ?
            ORDER BY m.FechaMovimiento DESC
        """, (int(id_producto),))

        columnas = [col[0] for col in cursor.description]

        for fila in cursor.fetchall():
            movimiento = dict(zip(columnas, fila))
            movimientos.append(movimiento)

    except Exception as e:
        print("Error al obtener movimientos:", e)
    finally:
        conn.close()

    return movimientos

