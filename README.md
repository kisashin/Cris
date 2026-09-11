SELECT DISTINCT Tipomovimiento, COUNT(*)
FROM historicomovimientos
WHERE archivocargue LIKE 'prueba%' OR archivocargue LIKE 'Cargue Col%'
GROUP BY Tipomovimiento;
