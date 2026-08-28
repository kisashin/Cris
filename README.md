-- Tipos y colacion de las dos columnas
SELECT 'historicomovimientos' t, c.name, ty.name tipo, c.max_length, c.collation_name
FROM sys.columns c 
JOIN sys.types ty ON ty.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.historicomovimientos') 
  AND c.name = 'Llavesiniestro'
UNION ALL
SELECT 'historico_inicial', c.name, ty.name, c.max_length, c.collation_name
FROM sys.columns c 
JOIN sys.types ty ON ty.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.historico_inicial') 
  AND c.name = 'Llavesiniestro';

-- La misma llave, en las dos tablas, con su longitud exacta
SELECT 'mov' origen, Llavesiniestro, LEN(Llavesiniestro) largo, 
       DATALENGTH(Llavesiniestro) bytes
FROM historicomovimientos 
WHERE NumeroSiniestro = '0802026A192761' AND Fechacontabilizacion IS NULL
UNION ALL
SELECT 'ini', Llavesiniestro, LEN(Llavesiniestro), DATALENGTH(Llavesiniestro)
FROM historico_inicial 
WHERE NumeroSiniestro = '0802026A192761';

-- Join directo sobre un caso concreto
SELECT COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.NumeroSiniestro = '0802026A192761';


SELECT * FROM historico_inicial WHERE NumeroSiniestro = '0192026A192673';
