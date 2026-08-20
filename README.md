SELECT name, create_date FROM tempdb.sys.tables WHERE name LIKE '##xmlSin%';

SELECT c.name FROM tempdb.sys.columns c
JOIN tempdb.sys.tables t ON t.object_id = c.object_id
WHERE t.name LIKE '##xmlSin%';
