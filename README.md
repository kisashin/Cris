SELECT TOP 3 NumeroSiniestro, 
       FechaMovimiento, 
       FechaMovimiento2,
       DATEDIFF(DAY, FechaMovimiento, FechaMovimiento2) AS diferencia_dias
FROM historicomovimientos
WHERE Fechacontabilizacion IS NULL
  AND Llavesiniestro IN (
      SELECT Llavesiniestro FROM historico_inicial WHERE Aval = 1);


      
