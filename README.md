SELECT DISTINCT hm.Tipomovimiento, LEN(hm.Tipomovimiento) AS largo, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Aval = 1
GROUP BY hm.Tipomovimiento, LEN(hm.Tipomovimiento);

-- La consulta corregida del periodo
SELECT DISTINCT CONVERT(nvarchar(6), hm.FechaMovimiento2, 112) AS periodo, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Aval = 1
GROUP BY CONVERT(nvarchar(6), hm.FechaMovimiento2, 112);

-- El INSERT del SP, replicado
SELECT COUNT(*)
FROM historicomovimientos
WHERE tipoMovimiento IN ('Aumento Reserva','Reserva Inicial - Re-Aseguradora')
  AND llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 1)
  AND fechacontabilizacion IS NULL 
  AND marcaavalpos IS NULL;
