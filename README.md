SELECT NumeroSiniestro, tipoMovimiento, vrmovimiento,
       FechaMovimiento2, fechacontabilizacion
FROM TBL_Historico_Movimientos
WHERE NumeroSiniestro IN ('0902026A193876', '0902026A193877')
ORDER BY NumeroSiniestro, FechaMovimiento2;
