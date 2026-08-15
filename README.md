SELECT o.name, o.type_desc, m.definition
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%archivoAsientoAval%'
   OR m.definition LIKE '%tmp_repavalcierre%';



SELECT t.name, t.is_disabled, OBJECT_NAME(t.parent_id) AS tabla
FROM sys.triggers t
WHERE OBJECT_NAME(t.parent_id) IN ('archivoAsientoAval','tmp_repavalcierre');


SELECT j.name AS job, j.enabled, s.step_id, s.step_name,
       s.subsystem, s.command, s.database_name
FROM msdb.dbo.sysjobs j
JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id
WHERE s.command LIKE '%archivoAsientoAval%'
   OR s.command LIKE '%AsientoAval%'
   OR s.command LIKE '%repavalcierre%'
   OR j.name LIKE '%aval%';



   SELECT j.name AS job, j.enabled, s.step_name, s.subsystem,
       LEFT(s.command, 500) AS comando
FROM msdb.dbo.sysjobs j
JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id
WHERE s.subsystem IN ('CmdExec','SSIS','PowerShell','ActiveScripting')
ORDER BY j.name, s.step_id;



SELECT COUNT(*) AS filas FROM dbo.archivoAsientoAval;
SELECT * FROM dbo.archivoAsientoAval;

SELECT c.name, ty.name AS tipo, c.max_length, c.is_nullable
FROM sys.columns c JOIN sys.types ty ON ty.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.archivoAsientoAval');
