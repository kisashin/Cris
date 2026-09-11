SELECT COUNT(*) 
FROM historico_inicial hi
JOIN historicomovimientos hm ON hm.Llavesiniestro = hi.Llavesiniestro
WHERE hi.NumeroSiniestro LIKE '%2026A%'
GROUP BY hm.archivocargue;
