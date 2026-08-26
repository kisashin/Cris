USE SiniestrosWp;
GO

CREATE TABLE dbo.archivoAsientoAvalXml (
    id              INT IDENTITY(1,1) NOT NULL,
    idLote          VARCHAR(50)    NOT NULL,
    periodo         VARCHAR(6)     NOT NULL,
    familia         VARCHAR(50)    NOT NULL,
    tipoMovimiento  VARCHAR(50)    NULL,
    nombreArchivo   VARCHAR(500)   NOT NULL,
    contenido       NVARCHAR(MAX)  NOT NULL,
    cantidadLineas  INT            NOT NULL,
    fechaproceso    DATETIME       NOT NULL,
    estado          VARCHAR(50)    NOT NULL,
    CONSTRAINT PK_archivoAsientoAvalXml PRIMARY KEY CLUSTERED (id)
);
GO


USE SiniestrosWp;
GO

CREATE TABLE dbo.archivoAsientoCardifXml (
    id              INT IDENTITY(1,1) NOT NULL,
    idLote          VARCHAR(50)    NOT NULL,
    periodo         VARCHAR(6)     NOT NULL,
    familia         VARCHAR(50)    NOT NULL,
    tipoMovimiento  VARCHAR(50)    NULL,
    nombreArchivo   VARCHAR(500)   NOT NULL,
    contenido       NVARCHAR(MAX)  NOT NULL,
    cantidadLineas  INT            NOT NULL,
    fechaproceso    DATETIME       NOT NULL,
    estado          VARCHAR(50)    NOT NULL,
    CONSTRAINT PK_archivoAsientoCardifXml PRIMARY KEY CLUSTERED (id)
);
GO
