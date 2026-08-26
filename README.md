CREATE TABLE dbo.archivoAsientoCentro (
    id              int IDENTITY(1,1) NOT NULL,
    idLote          nvarchar(36) NOT NULL,
    periodo         nvarchar(6) NULL,
    tipoMovimiento  nvarchar(50) NULL,
    nombreArchivo   nvarchar(500) NULL,
    contenido       varchar(max) NULL,
    cantidadLineas  int NULL,
    fechaproceso    datetime NULL,
    estado          nvarchar(500) NULL,
    CONSTRAINT PK_archivoAsientoCentro PRIMARY KEY CLUSTERED (id)
);
GO

CREATE INDEX IX_archivoAsientoCentro_fechaproceso
    ON dbo.archivoAsientoCentro (fechaproceso DESC, id DESC);
GO

CREATE INDEX IX_archivoAsientoCentro_lote
    ON dbo.archivoAsientoCentro (idLote);
GO
