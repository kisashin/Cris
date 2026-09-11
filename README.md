SELECT hm.NumeroSiniestro, hm.Tipomovimiento,
       hm.FechaMovimiento, hm.FechaMovimiento2,
       hm.Fechaocurrencia, hm.Fechaavisocardif
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Aval = 1;
