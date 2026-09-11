-- 1. Periodo que usa Aval vs periodo de tus movimientos
SELECT CONVERT(nvarchar(6), getdate()-5, 112) AS periodo_aval;

SELECT DISTINCT CONVERT(nvarchar(6), FechaMovimiento2, 112) AS periodo_mov, COUNT(*)
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL
GROUP BY CONVERT(nvarchar(6), FechaMovimiento2, 112);

-- 2. Ramo, producto y si esta parametrizado
SELECT hm.NumeroSiniestro, hm.Socio, hm.Ramo, hm.CodProducto, hm.Tipomovimiento,
       CASE WHEN hm.CodProducto IN (
            SELECT PRODUCTO FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
            WHERE ramo = 7 AND GRUPO = 'A') 
       THEN 'SI' ELSE 'NO' END AS producto_grupo_A
FROM historicomovimientos hm
WHERE hm.Fechacontabilizacion IS NULL;

-- 3. Que quedo en la tabla de trabajo despues del intento
SELECT COUNT(*) FROM tmpsiniestros;
SELECT COUNT(*) FROM HistoricoasientosPru;


SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
