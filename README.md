SELECT o.name
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%exec%sp_XMLAsientosPru%'
  AND o.name <> 'sp_XMLAsientosPru'
  AND o.name NOT LIKE 'sp_XMLAsientosPru%';


  
