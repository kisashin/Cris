SELECT Tipomovimiento, Socio, Codsocio, Codproducto, COUNT(*)
FROM historicomovimientos
WHERE Tipomovimiento LIKE 'Reserva Inicial%'
  AND archivocargue LIKE 'prueba%'
GROUP BY Tipomovimiento, Socio, Codsocio, Codproducto
ORDER BY Tipomovimiento;
