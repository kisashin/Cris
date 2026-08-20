SELECT ISNULL(a.name, b.name) AS columna,
       ta.name + '(' + CAST(a.max_length/2 AS varchar) + ')' AS colombia,
       tb.name + '(' + CAST(b.max_length/2 AS varchar) + ')' AS peru
FROM sys.columns a
FULL JOIN sys.columns b
       ON b.object_id = OBJECT_ID('dbo.tmpsiniestros_ext')
      AND LTRIM(RTRIM(b.name)) = LTRIM(RTRIM(a.name))
LEFT JOIN sys.types ta ON ta.user_type_id = a.user_type_id
LEFT JOIN sys.types tb ON tb.user_type_id = b.user_type_id
WHERE a.object_id = OBJECT_ID('dbo.tmpsiniestros')
   OR b.object_id = OBJECT_ID('dbo.tmpsiniestros_ext');


SELECT '[' + name + ']' AS nombre_exacto, LEN(name) AS largo
FROM sys.columns WHERE object_id = OBJECT_ID('dbo.tmpsiniestros_ext') AND name LIKE 'Cobertura%';   
