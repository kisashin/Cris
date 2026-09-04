USE SiniestrosWp;

SELECT idusuario, idautorizador, COUNT(*) AS total,
       MIN(Fechaproceso) AS desde, MAX(Fechaproceso) AS hasta
FROM novedadhistoricoindividual
GROUP BY idusuario, idautorizador
ORDER BY total DESC;

SELECT estado, tiponovedad, COUNT(*) AS total
FROM novedadhistoricoindividual
GROUP BY estado, tiponovedad;

SELECT TOP 20 CIE, COUNT(*) AS total
FROM historicomovimientos
WHERE CIE IS NOT NULL AND LTRIM(RTRIM(CIE)) <> ''
GROUP BY CIE ORDER BY total DESC;
