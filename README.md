SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NOT NULL;

SELECT TOP 20 NumeroSiniestro, Tipomovimiento, Fechacontabilizacion, archivocargue
FROM historicomovimientos 
WHERE NumeroSiniestro IN ('0802026A192761','0192026A192673','0102026A192436')
ORDER BY NumeroSiniestro;

-- Los 1087 sin contabilizar, ¿de que cargue son?
SELECT archivocargue, COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL 
GROUP BY archivocargue;
