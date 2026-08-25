-- 1. Cómo tradujo las etiquetas
SELECT tipoMovimiento, COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL GROUP BY tipoMovimiento;

-- 2. El que de verdad importa
SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);

-- 3. Periodo
SELECT CONVERT(nvarchar(6), FechaMovimiento2, 112) periodo, COUNT(*)
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
GROUP BY CONVERT(nvarchar(6), FechaMovimiento2, 112);

