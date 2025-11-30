use InventarioDB;
go

CREATE TABLE MovimientosInventario (
    IdMovimiento INT IDENTITY(1,1) PRIMARY KEY,
    IdProducto INT NOT NULL,
    TipoMovimiento VARCHAR(10) NOT NULL, -- 'ENTRADA' o 'SALIDA'
    Cantidad INT NOT NULL,
    FechaMovimiento DATETIME NOT NULL DEFAULT GETDATE(),
    Referencia VARCHAR(100) NULL,        -- factura, vale, etc.
    Observaciones VARCHAR(255) NULL,

    StockAnterior INT NULL,
    StockNuevo INT NULL,

    CONSTRAINT FK_Movimientos_Productos
        FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto)
);