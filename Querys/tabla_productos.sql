USE InventarioDB;
GO

CREATE TABLE Productos (
    IdProducto INT IDENTITY(1,1) PRIMARY KEY,
    Codigo VARCHAR(50) NOT NULL,
    Nombre VARCHAR(150) NOT NULL,
    Categoria VARCHAR(100) NULL,
    Proveedor VARCHAR(150) NULL,
    PrecioCompra DECIMAL(18,2) NOT NULL,
    PrecioVenta DECIMAL(18,2) NOT NULL,
    StockActual INT NOT NULL DEFAULT 0,
    StockMinimo INT NOT NULL DEFAULT 0,
    Activo BIT NOT NULL DEFAULT 1,
    FechaCreacion DATETIME NOT NULL DEFAULT GETDATE()
);

UPDATE Productos SET StockMinimo = 8 WHERE IdProducto = 1;  
UPDATE Productos SET StockMinimo = 10 WHERE IdProducto = 2; 
UPDATE Productos SET StockMinimo = 5 WHERE IdProducto = 3;  
UPDATE Productos SET StockMinimo = 2  WHERE IdProducto = 4; 


