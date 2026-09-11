-- ¿Se cargaron los 10?
SELECT archivocargue, COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL 
GROUP BY archivocargue;

-- ¿De que socios son?
SELECT Socio, Tipomovimiento, COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL 
GROUP BY Socio, Tipomovimiento;

-- ¿Tienen apertura y de que lado?
SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
