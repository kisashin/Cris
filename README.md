SELECT Tipomovimiento, Socio, Codsocio, Codproducto, COUNT(*)
FROM historicomovimientos
WHERE Tipomovimiento LIKE 'Reserva Inicial%'
  AND Fechacontabilizacion IS NULL
GROUP BY Tipomovimiento, Socio, Codsocio, Codproducto
ORDER BY Tipomovimiento;

SELECT TOP 30 Tipomovimiento, Socio, Codsocio, Codproducto, archivocargue
FROM historicomovimientos
WHERE Tipomovimiento LIKE 'Reserva Inicial%'
ORDER BY fechacargue DESC;
