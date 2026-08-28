SELECT TOP 10 hm.NumeroSiniestro, hm.Cobertura, hm.Llavesiniestro, hm.socio
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.archivocargue = 'Cargue Col 11 08 2026.xlsx'
  AND hi.Llavesiniestro IS NULL;
