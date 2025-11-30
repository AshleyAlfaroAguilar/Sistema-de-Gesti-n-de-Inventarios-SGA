from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from functools import wraps

# Importar la función para traer productos
from models.productos import obtener_todos_los_productos
from flask import request, redirect, url_for, flash

from models.productos import (
    obtener_todos_los_productos,
    insertar_producto,
    obtener_producto_por_id,
    actualizar_producto,
    eliminar_producto,
    obtener_productos_stock_bajo,
)

from models.movimientos import registrar_movimiento, obtener_movimientos_por_producto
from models.usuarios import validar_usuario

# Cargar variables desde .env
load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-dev-123")


#AUTHENTICATION 

def login_requerido(vista_func):
    @wraps(vista_func)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return vista_func(*args, **kwargs)
    return wrapper

def rol_requerido(*roles_permitidos):
    def decorador(vista_func):
        @wraps(vista_func)
        def wrapper(*args, **kwargs):
            if 'usuario_id' not in session:
                return redirect(url_for('login'))

            rol_usuario = session.get('usuario_rol', '').upper()

            if rol_usuario not in [r.upper() for r in roles_permitidos]:
                # Si no tiene rol permitido, lo mandamos al home
                return redirect(url_for('home'))

            return vista_func(*args, **kwargs)
        return wrapper
    return decorador



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos al inicio
    if 'usuario_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = validar_usuario(username, password)

        if usuario:
            # Guardar datos básicos en sesión
            session['usuario_id'] = usuario['IdUsuario']
            session['usuario_nombre'] = usuario['NombreCompleto']
            session['usuario_rol'] = usuario['Rol']

            return redirect(url_for('home'))
        else:
            # Error simple por ahora
            error = "Usuario o contraseña incorrectos."
            return render_template('login.html', error=error)

    # Si es GET, solo mostramos el formulario
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




# Ruta principal (home)
@app.route('/')
@login_requerido
def home():
    return render_template('index.html')

#PRODUCTOS 

#listado de productos
@app.route('/productos')
@login_requerido
def listar_productos():
    productos = obtener_todos_los_productos()
    return render_template('productos.html', productos=productos)

# Ruta para mostrar formulario de nuevo producto
@app.route('/productos/nuevo', methods=['GET'])
@login_requerido
def nuevo_producto():
    return render_template('nuevo_producto.html')

# Ruta para guardar producto
@app.route('/productos/guardar', methods=['POST'])
@login_requerido
def guardar_producto():

    codigo = request.form['codigo']
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    proveedor = request.form['proveedor']
    precio_compra = request.form['precio_compra']
    precio_venta = request.form['precio_venta']
    stock = request.form['stock']

    insertar_producto(
        codigo,
        nombre,
        categoria,
        proveedor,
        precio_compra,
        precio_venta,
        stock
    )

    return redirect(url_for('listar_productos'))    


# Ruta para mostrar el formulario de edición
@app.route('/productos/editar/<int:id_producto>', methods=['GET'])
@login_requerido
@rol_requerido('ADMIN', 'SUPERVISOR')
def editar_producto(id_producto):
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        # Si no existe, vuelve al listado
        return redirect(url_for('listar_productos'))
    return render_template('editar_producto.html', producto=producto)

# Ruta para actualizar los datos en la BD
@app.route('/productos/actualizar', methods=['POST'])
@login_requerido
@rol_requerido('ADMIN', 'SUPERVISOR')
def actualizar_producto_route():
    id_producto = request.form['id_producto']
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    proveedor = request.form['proveedor']
    precio_compra = request.form['precio_compra']
    precio_venta = request.form['precio_venta']
    stock = request.form['stock']

    actualizar_producto(
        id_producto,
        codigo,
        nombre,
        categoria,
        proveedor,
        precio_compra,
        precio_venta,
        stock
    )

    return redirect(url_for('listar_productos'))

@app.route('/productos/eliminar/<int:id_producto>', methods=['GET'])
@login_requerido
@rol_requerido('ADMIN', 'SUPERVISOR')
def eliminar_producto_route(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for('listar_productos'))

#MOVIEMIENTOS 

# Formulario para registrar un movimiento (entrada/salida)
@app.route('/movimientos/nuevo', methods=['GET'])
@login_requerido
def nuevo_movimiento():
    # Necesitamos la lista de productos para elegir a cuál aplicar el movimiento
    productos = obtener_todos_los_productos()
    return render_template('nuevo_movimiento.html', productos=productos)

# Guardar el movimiento en la BD
@app.route('/movimientos/guardar', methods=['POST'])
@login_requerido
def guardar_movimiento():
    id_producto = request.form['id_producto']
    tipo_movimiento = request.form['tipo_movimiento']  # ENTRADA / SALIDA
    cantidad = request.form['cantidad']
    referencia = request.form.get('referencia')
    observaciones = request.form.get('observaciones')

    ok = registrar_movimiento(
        id_producto,
        tipo_movimiento,
        cantidad,
        referencia,
        observaciones
    )

    # Por ahora, si algo sale mal solo regresamos al listado
    return redirect(url_for('listar_productos'))

# Historial de movimientos de un producto
@app.route('/movimientos/producto/<int:id_producto>', methods=['GET'])
@login_requerido
def movimientos_por_producto(id_producto):
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        return redirect(url_for('listar_productos'))

    movimientos = obtener_movimientos_por_producto(id_producto)
    return render_template(
        'movimientos_producto.html',
        producto=producto,
        movimientos=movimientos
    )
    
#REPORTES 
@app.route('/reportes/stock-bajo')
@login_requerido
def reporte_stock_bajo():
    productos = obtener_productos_stock_bajo()
    return render_template('reporte_stock_bajo.html', productos=productos)
    

if __name__ == '__main__':
    app.run(debug=True)


