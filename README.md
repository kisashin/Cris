EXEC sp_helptext 'dbo.sp_XMLAsientosPru';
EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_ReasegAlfa';
EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_ReasegCardif';
EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_CoaseguroC';
EXEC sp_helptext 'dbo.sp_contabiliza_aval';
EXEC sp_helptext 'dbo.sp_contabiliza_cardif';
EXEC sp_helptext 'dbo.sp_contabiliza_coaseguro';

--liquibase formatted sql

--changeset j36147:crear_archivoAsientoAvalXml dbms:mssql
CREATE TABLE SiniestrosWp.dbo.archivoAsientoAvalXml (
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
)
--rollback DROP TABLE SiniestrosWp.dbo.archivoAsientoAvalXml

--changeset j36147:crear_archivoAsientoCardifXml dbms:mssql
CREATE TABLE SiniestrosWp.dbo.archivoAsientoCardifXml (
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
)
--rollback DROP TABLE SiniestrosWp.dbo.archivoAsientoCardifXml

USE [SiniestrosWp];
GO

DROP TABLE dbo.archivoAsientoAvalXml;
DROP TABLE dbo.archivoAsientoCardifXml;
GO
