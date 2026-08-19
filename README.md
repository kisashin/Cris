SELECT convert(nvarchar(6),FechaMovimiento2,112) periodo, tipoMovimiento, count(*), sum(vrmovimiento)
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
GROUP BY convert(nvarchar(6),FechaMovimiento2,112), tipoMovimiento
ORDER BY 1;
