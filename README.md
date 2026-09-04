USE SiniestrosWp;

SELECT COUNT(*) AS filas, COUNT(DISTINCT id) AS ids_distintos,
       MIN(id) AS id_min, MAX(id) AS id_max,
       MIN(IDCARVAJAL) AS carv_min, MAX(IDCARVAJAL) AS carv_max
FROM historicomovimientos;

SELECT n.codigo, n.Id, n.NumeroSiniestro, n.Llavesiniestro,
       COUNT(h.IDCARVAJAL) AS match_carvajal
FROM novedadhistoricoindividual n
LEFT JOIN historicomovimientos h ON h.IDCARVAJAL = n.Id
GROUP BY n.codigo, n.Id, n.NumeroSiniestro, n.Llavesiniestro;

SELECT n.codigo, n.NumeroSiniestro,
       COUNT(h.IDCARVAJAL) AS match_por_numsiniestro
FROM novedadhistoricoindividual n
LEFT JOIN historicomovimientos h ON h.NumeroSiniestro = n.NumeroSiniestro
GROUP BY n.codigo, n.NumeroSiniestro;

SELECT MIN(fechacargue) AS primer_cargue, MAX(fechacargue) AS ultimo_cargue,
       COUNT(DISTINCT archivocargue) AS archivos
FROM historicomovimientos;
