SELECT OBJECT_SCHEMA_NAME(o.object_id) AS esquema,
       OBJECT_NAME(o.object_id)        AS objeto,
       o.type_desc
FROM sys.sql_modules m
INNER JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%archivoAsientoAval%'
   OR m.definition LIKE '%archivoAsientoCardif%'
   OR m.definition LIKE '%tmp_repavalcierre%';

SELECT OBJECT_NAME(object_id) FROM sys.sql_modules
WHERE definition LIKE '%xp_cmdshell%' OR definition LIKE '%bcp %';

SELECT j.name, s.step_name, s.command
FROM msdb.dbo.sysjobs j JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id;

SELECT * FROM dbo.archivoAsientoAval;
SELECT * FROM dbo.archivoAsientoCardif;


SELECT j.name AS job,
       j.enabled,
       s.step_id,
       s.step_name,
       s.subsystem,
       s.database_name,
       s.command
FROM msdb.dbo.sysjobs j
INNER JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id
ORDER BY j.name, s.step_id;
