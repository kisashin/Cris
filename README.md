-- ¿Cuantos del cargue siguen con fecha de otro dia?
SELECT Fechacontabilizacion, COUNT(*) 
FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND Fechacontabilizacion IS NOT NULL
GROUP BY Fechacontabilizacion;

-- ¿Cuantos tienen marcaavalpos?
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NOT NULL;
