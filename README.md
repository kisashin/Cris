--liquibase formatted sql
--changeset j36147:HU_Reaseguro_566_archivoAsientoReaseguro_20260903_01 stripComments:false dbms:mssql

USE [CardifWP]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO

IF OBJECT_ID('dbo.archivoAsientoReaseguro','U') IS NULL
BEGIN
    CREATE TABLE dbo.archivoAsientoReaseguro (
        id              INT IDENTITY(1,1) NOT NULL,
        producto        VARCHAR(10)   NOT NULL,
        tipoDiario      VARCHAR(10)   NOT NULL,
        periodoContable VARCHAR(10)   NOT NULL,
        nombreArchivo   VARCHAR(100)  NOT NULL,
        contenido       NVARCHAR(MAX) NOT NULL,
        fechaGeneracion DATETIME      NOT NULL,
        usuario         VARCHAR(100)  NULL,
        CONSTRAINT PK_archivoAsientoReaseguro PRIMARY KEY CLUSTERED (id),
        CONSTRAINT UQ_archivoAsientoReaseguro UNIQUE NONCLUSTERED (producto, tipoDiario, periodoContable)
    )
END

--rollback DROP TABLE IF EXISTS dbo.archivoAsientoReaseguro
