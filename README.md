SELECT 
    c.name AS columna,
    t.name AS tipo,
    c.max_length,
    c.is_nullable
FROM sys.columns c
JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.vw_mov_cardif_ext')
ORDER BY c.column_id;
