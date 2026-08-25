ALTER TABLE dbo.archivoAsientoCentro ALTER COLUMN nombreArchivo nvarchar(10);


SELECT COUNT(*) FROM dbo.archivoAsientoCentro;

SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);

  ALTER TABLE dbo.archivoAsientoCentro ALTER COLUMN nombreArchivo nvarchar(500);


  SET STATISTICS TIME ON;
BEGIN TRAN;
EXEC dbo.sp_contabiliza_cardifCentro;
ROLLBACK;
SET STATISTICS TIME OFF;
