BEGIN TRAN;
UPDATE TBL_Historico_Movimientos SET fechacontabilizacion = NULL
WHERE CONVERT(nvarchar(6), FechaMovimiento2, 112) = '202608';
SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);
COMMIT;

SELECT id, idLote, tipoMovimiento FROM dbo.archivoAsientoCentro ORDER BY id;

SELECT id, idLote, tipoMovimiento, cantidadLineas, fechaproceso
FROM dbo.archivoAsientoCentro ORDER BY id;
