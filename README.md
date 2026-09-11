SELECT NumeroSiniestro, Tipomovimiento, Socio, marcaavalpos
FROM historicomovimientos
WHERE archivocargue = 'prueba 2';

UPDATE historicomovimientos 
SET marcaavalpos = NULL 
WHERE archivocargue = 'prueba 2';

UPDATE archivodatos SET estado = 'PENDIENTE' WHERE id = 1;

SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
