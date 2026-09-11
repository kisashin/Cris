SELECT NumeroSiniestro, Tipomovimiento,
       FechaMovimiento, FechaMovimiento2,
       Fechaocurrencia, Fechaavisocardif
FROM historicomovimientos
WHERE Fechacontabilizacion IS NULL
  AND Llavesiniestro IN (
      SELECT Llavesiniestro FROM historico_inicial WHERE Aval = 1);
