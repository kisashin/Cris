SELECT OBJECT_NAME(object_id) AS objeto
FROM sys.sql_modules
WHERE definition LIKE '%FechaMovimiento2%'
  AND (definition LIKE '%dateadd%' OR definition LIKE '%DATEADD%');
