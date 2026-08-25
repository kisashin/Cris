SELECT tipoMovimiento, cantidadLineas, nombreArchivo, estado
FROM dbo.archivoAsientoCentro ORDER BY id;

SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);
