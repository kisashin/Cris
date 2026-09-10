SELECT COUNT(*) FROM historico_inicial WHERE NumeroSiniestro LIKE '%2026A%';

SELECT MAX(IDCARVAJAL) FROM historico_inicial;


SELECT COUNT(*) FROM historico_inicial 
WHERE Llavesiniestro IN (
  SELECT Llavesiniestro FROM historicomovimientos 
  WHERE archivocargue = 'Cargue Col 07 09 2026.xlsx');
