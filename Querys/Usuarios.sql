use InventarioDB;
go

CREATE TABLE Usuarios (
    IdUsuario INT IDENTITY(1,1) PRIMARY KEY,
    Username  VARCHAR(50) NOT NULL UNIQUE,
    Password  VARCHAR(255) NOT NULL,
    NombreCompleto VARCHAR(150) NOT NULL,
    Rol      VARCHAR(20) NOT NULL,  -- ADMIN, OPERADOR, SUPERVISOR
    Activo   BIT NOT NULL DEFAULT 1,
    FechaCreacion DATETIME NOT NULL DEFAULT GETDATE()
);

-- Usuario admin inicial (solo para pruebas)
--INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol, Activo)
--VALUES ('admin', 'admin123', 'Administrador General', 'ADMIN', 1);

--INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol, Activo)
--VALUES ('Operador', 'oper123', 'Operador', 'OPERADOR', 1);

INSERT INTO Usuarios (Username, Password, NombreCompleto, Rol, Activo)
VALUES ('supervisor', 'sup123', 'Supervisor General', 'SUPERVISOR', 1);
