-- ¿Existe la llave sin espacios?
SELECT COUNT(*) FROM historico_inicial 
WHERE Llavesiniestro LIKE '0192026A192673%';

-- ¿Cuantas del cargue nuevo tienen contraparte, normalizando espacios?
SELECT COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi 
  ON REPLACE(hi.Llavesiniestro, ' ', '') = REPLACE(hm.Llavesiniestro, ' ', '')
WHERE hm.Fechacontabilizacion IS NULL;

-- ¿Que hay en historico_inicial del periodo actual?
SELECT TOP 10 Llavesiniestro, NumeroSiniestro, Aval 
FROM historico_inicial 
WHERE NumeroSiniestro LIKE '%2026A19%';
