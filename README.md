SELECT c.column_id, c.name, t.name AS tipo, c.max_length, c.precision, c.scale, c.is_nullable
FROM tempdb.sys.columns c
JOIN tempdb.sys.tables tb ON tb.object_id = c.object_id
JOIN tempdb.sys.types t ON t.user_type_id = c.user_type_id
WHERE tb.name LIKE '##xmlSin%'
ORDER BY c.column_id;
