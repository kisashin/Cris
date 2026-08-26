--liquibase formatted sql
--changeset j36147:COIMPLUT-35258_Create_Table_archivoAsientoCentro_20260826_01

IF OBJECT_ID('dbo.archivoAsientoCentro', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[archivoAsientoCentro](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [idLote] [nvarchar](36) COLLATE Modern_Spanish_CI_AS NOT NULL,
        [periodo] [nvarchar](6) COLLATE Modern_Spanish_CI_AS NULL,
        [tipoMovimiento] [nvarchar](50) COLLATE Modern_Spanish_CI_AS NULL,
        [nombreArchivo] [nvarchar](500) COLLATE Modern_Spanish_CI_AS NULL,
        [contenido] [varchar](max) COLLATE Modern_Spanish_CI_AS NULL,
        [cantidadLineas] [int] NULL,
        [fechaproceso] [datetime] NULL,
        [estado] [nvarchar](500) COLLATE Modern_Spanish_CI_AS NULL,
        CONSTRAINT [PK_archivoAsientoCentro] PRIMARY KEY CLUSTERED
        (
            [id] ASC
        ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
    ) ON [PRIMARY]
END

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_archivoAsientoCentro_lote' AND object_id = OBJECT_ID('dbo.archivoAsientoCentro'))
BEGIN
    CREATE NONCLUSTERED INDEX [IX_archivoAsientoCentro_lote] ON [dbo].[archivoAsientoCentro]
    (
        [idLote] ASC
    ) ON [PRIMARY]
END

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_archivoAsientoCentro_fechaproceso' AND object_id = OBJECT_ID('dbo.archivoAsientoCentro'))
BEGIN
    CREATE NONCLUSTERED INDEX [IX_archivoAsientoCentro_fechaproceso] ON [dbo].[archivoAsientoCentro]
    (
        [fechaproceso] DESC,
        [id] DESC
    ) ON [PRIMARY]
END
