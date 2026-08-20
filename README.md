SELECT DISTINCT LEN([Cobertura_afectada ]) AS largo, [Cobertura_afectada ]
FROM dbo.vw_mov_cardif_ext WITH (NOLOCK)
WHERE LEN([Cobertura_afectada ]) > 50
ORDER BY 1 DESC;

SELECT OBJECT_NAME(c.object_id) AS tabla, c.name, t.name AS tipo, c.max_length
FROM sys.columns c
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id IN (
    OBJECT_ID('dbo.tmpsiniestros_ext'),
    OBJECT_ID('dbo.tmpsiniestros'),
    OBJECT_ID('dbo.historicomovimientos_ext')
)
AND c.name LIKE 'Cobertura%'
ORDER BY tabla;
