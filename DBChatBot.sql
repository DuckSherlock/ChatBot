create database CS

use CS

CREATE TABLE Usuarios (
    Id INT PRIMARY KEY IDENTITY(1,1),
	Dni NVARCHAR(8),
    Nombre NVARCHAR(100),
    Apellidos NVARCHAR(100),
	Universidad NVARCHAR(100),
	Carrera NVARCHAR(50),
    FechaCreacion DATETIME DEFAULT GETDATE()
);

go

select * from Usuarios
delete from Usuarios where Id=1