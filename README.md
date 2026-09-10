--liquibase formatted sql

--changeset j36147:crear_archivoReporteAvalExcel dbms:mssql
CREATE TABLE SiniestrosWp.dbo.archivoReporteAvalExcel (
    id             INT IDENTITY(1,1) NOT NULL,
    idLote         VARCHAR(50)    NOT NULL,
    periodo        VARCHAR(6)     NOT NULL,
    nombreArchivo  VARCHAR(500)   NOT NULL,
    contenido      VARBINARY(MAX) NOT NULL,
    cantidadFilas  INT            NOT NULL,
    fechaproceso   DATETIME       NOT NULL,
    estado         VARCHAR(50)    NOT NULL,
    CONSTRAINT PK_archivoReporteAvalExcel PRIMARY KEY CLUSTERED (id)
)
--rollback DROP TABLE SiniestrosWp.dbo.archivoReporteAvalExcel
