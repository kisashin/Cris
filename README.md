-- Confirmar cuantos quedan sin apertura
SELECT COUNT(*) 
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Llavesiniestro IS NULL;

-- Cuantas aperturas entraron con este cargue
SELECT COUNT(*) FROM historico_inicial;

-- Comparar una llave de cada lado
SELECT TOP 5 Llavesiniestro, NumeroSiniestro, Cobertura 
FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 07 09 2026.xlsx';

SELECT TOP 5 Llavesiniestro, NumeroSiniestro, Cobertura 
FROM historico_inicial 
ORDER BY IDCARVAJAL DESC;




SELECT name FROM sys.tables 
WHERE name IN ('archivoAsientoAvalXml','archivoAsientoCardifXml','archivoReporteAvalExcel');



USE [SiniestrosWp];
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
