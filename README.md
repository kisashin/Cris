WITH col AS (
    SELECT c.object_id,
           LTRIM(RTRIM(c.name)) AS columna,
           t.name AS tipo,
           CASE WHEN c.max_length = -1 THEN -1
                WHEN t.name LIKE 'n[cv]%' THEN c.max_length / 2
                ELSE c.max_length END AS largo
    FROM sys.columns c
    JOIN sys.types t ON t.user_type_id = c.user_type_id
)
SELECT ISNULL(co.columna, pe.columna) AS columna,
       ISNULL(co.tipo + '(' + CAST(co.largo AS varchar) + ')', '-- NO EXISTE --') AS colombia,
       ISNULL(pe.tipo + '(' + CAST(pe.largo AS varchar) + ')', '-- NO EXISTE --') AS peru
FROM       (SELECT * FROM col WHERE object_id = OBJECT_ID('dbo.tmpsiniestros'))     co
FULL JOIN  (SELECT * FROM col WHERE object_id = OBJECT_ID('dbo.tmpsiniestros_ext')) pe
       ON pe.columna = co.columna
WHERE co.columna IS NULL
   OR pe.columna IS NULL
   OR co.tipo <> pe.tipo
   OR co.largo <> pe.largo
ORDER BY 1;
