CREATE TABLE dbo.archivoAsientoReaseguro (
    id              INT IDENTITY(1,1) NOT NULL,
    producto        VARCHAR(10)   NOT NULL,
    tipoDiario      VARCHAR(10)   NOT NULL,
    periodoContable VARCHAR(10)   NOT NULL,
    nombreArchivo   VARCHAR(100)  NOT NULL,
    contenido       NVARCHAR(MAX) NOT NULL,
    fechaGeneracion DATETIME      NOT NULL,
    usuario         VARCHAR(100)  NULL,
    CONSTRAINT PK_archivoAsientoReaseguro PRIMARY KEY (id),
    CONSTRAINT UQ_archivoAsientoReaseguro UNIQUE (producto, tipoDiario, periodoContable)
);
