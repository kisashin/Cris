SELECT NumeroSiniestro, Tipomovimiento, Socio, marcaavalpos
FROM historicomovimientos
WHERE archivocargue = 'prueba 2';


SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
