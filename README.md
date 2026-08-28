-- ¿Estos siniestros existen en historico_inicial con otra cobertura?
SELECT * FROM historico_inicial 
WHERE NumeroSiniestro IN ('0392026A192110','0082026A153294','0072026A191953');

-- ¿Que rango de fechas cubre historico_inicial?
SELECT MIN(NumeroSiniestro), MAX(NumeroSiniestro), COUNT(*) 
FROM historico_inicial;

-- ¿Los 650 son todos de siniestros viejos?
SELECT COUNT(DISTINCT hm.NumeroSiniestro)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.archivocargue = 'Cargue Col 11 08 2026.xlsx'
  AND hi.Llavesiniestro IS NULL;
