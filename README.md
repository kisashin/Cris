-- ¿Cuantos movimientos de Reserva Inicial hay pendientes?
SELECT Tipomovimiento, marcaavalpos, COUNT(*)
FROM historicomovimientos
WHERE Tipomovimiento LIKE 'Reserva Inicial%'
GROUP BY Tipomovimiento, marcaavalpos;

-- ¿Las llaves de tus 8 estan en historico_inicial?
SELECT hm.NumeroSiniestro, hm.Tipomovimiento, hm.Llavesiniestro,
       CASE WHEN hi.Llavesiniestro IS NULL THEN 'NO' ELSE 'SI' END AS tiene_apertura
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
  AND hm.Tipomovimiento LIKE 'Reserva Inicial%';
