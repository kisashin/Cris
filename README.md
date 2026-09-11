SELECT hm.NumeroSiniestro, hm.Cobertura, hm.Socio, hm.Ramo, 
       hm.CodProducto, hm.Tipomovimiento, hm.Llavesiniestro
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Llavesiniestro IS NULL;


SELECT hm.NumeroSiniestro, hm.Cobertura, hm.Tipomovimiento, hi.Aval
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL;
