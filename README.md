SELECT Identificacion, COUNT(*) AS veces, COUNT(DISTINCT Nombre) AS nombres_distintos
FROM dbo.historicoterceros WITH (NOLOCK)
WHERE Proceso = 'PERU'
GROUP BY Identificacion
HAVING COUNT(*) > 1
ORDER BY veces DESC;
