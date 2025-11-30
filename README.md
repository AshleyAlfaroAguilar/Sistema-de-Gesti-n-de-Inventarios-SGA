# Sistema de Gestión de Inventarios (SGA)
### *ElectroDistribuciones S.A.*

## Descripción del Proyecto
El **Sistema de Gestión de Inventarios (SGA)** es una aplicación web desarrollada en **Python (Flask)** y **SQL Server**, diseñada para la administración eficiente de productos, control de movimientos de inventario, generación de reportes y gestión de accesos mediante roles.

Este proyecto fue elaborado como parte del **Proyecto del Semestre**, aplicando buenas prácticas de desarrollo, modularidad, seguridad, manejo de base de datos y arquitectura limpia.

## Tecnologías Utilizadas
- Python 3.x
- Flask
- HTML + CSS
- SQL Server
- PyODBC
- Virtualenv (venv)

## Estructura del Proyecto
```
inventario_sga/
│
├── app.py
├── .env
│
├── models/
│   ├── db.py
│   ├── productos.py
│   ├── movimientos.py
│   └── usuarios.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── productos.html
│   ├── nuevo_producto.html
│   ├── editar_producto.html
│   ├── nuevo_movimiento.html
│   ├── movimientos_producto.html
│   └── reporte_stock_bajo.html
│
└── static/
    └── css/
        └── style.css
```

## Usuarios y Contraseñas
| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| **ADMIN** | admin | admin123 | CRUD productos, movimientos y reportes |
| **SUPERVISOR** | supervisor | sup123 | CRUD productos, movimientos y reportes |
| **OPERADOR** | operador | oper123 | Movimientos + reportes, sin edición de productos |

## Instalación y Ejecución

### Clonar el repositorio
```
git clone <URL_DEL_REPOSITORIO>
cd inventario_sga
```

### Crear y activar entorno virtual
Windows:
```
python -m venv venv
venv\Scripts\activate
```

### Instalar dependencias
```
pip install -r requirements.txt
```

### Crear archivo .env
```
DB_SERVER=nombre del servidor
DB_NAME=InventarioDB
DB_DRIVER=ODBC Driver 17 for SQL Server
FLASK_SECRET_KEY=super_secreto_123
```

### Configurar base de datos
```
CREATE DATABASE InventarioDB;
```

Crear usuarios iniciales:
```
INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol)
VALUES ('admin', 'admin123', 'Administrador General', 'ADMIN');

INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol)
VALUES ('supervisor', 'sup123', 'Supervisor General', 'SUPERVISOR');

INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol)
VALUES ('operador', 'oper123', 'Operador de Inventario', 'OPERADOR');
```

### Ejecutar aplicación
```
python app.py
```

Abrir navegador:  
http://127.0.0.1:5000

## Control de Roles
- **ADMIN:** CRUD productos, movimientos y reportes  
- **SUPERVISOR:** CRUD productos, movimientos y reportes  
- **OPERADOR:** Movimientos y reportes  

## Funcionalidades Principales
✔️ Login con roles  
✔️ Gestión de productos (CRUD)  
✔️ Movimientos de inventario  
✔️ Reportes e historial  
✔️ Alerta de stock bajo  

## Créditos
Proyecto desarrollado por:  
**Ashley Dayane Alfaro Aguilar carné 202301982**
**Byron Rodolfo Maldonado Palacios carné 202300076**  
Proyecto del Semestre – *ElectroDistribuciones S.A.*
