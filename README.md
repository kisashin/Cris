SELECT hi.Aval, hm.marcaavalpos, COUNT(*)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval, hm.marcaavalpos;

SELECT DISTINCT Socio, LEN(Socio) AS largo
FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;
