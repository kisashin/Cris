SELECT OBJECT_NAME(object_id) AS objeto, type_desc
FROM sys.sql_modules m JOIN sys.objects o USING... -- la que te pasé, con:
--   definition LIKE '%archivoAsientoAval%' OR '%archivoAsientoCardif%'

SELECT OBJECT_NAME(object_id) FROM sys.sql_modules
WHERE definition LIKE '%xp_cmdshell%' OR definition LIKE '%bcp %';

SELECT j.name, s.step_name, s.command
FROM msdb.dbo.sysjobs j JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id;

SELECT * FROM dbo.archivoAsientoAval;
SELECT * FROM dbo.archivoAsientoCardif;
