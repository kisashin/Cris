SELECT name, type_desc, create_date, modify_date
FROM sys.objects
WHERE type IN ('P','FN','TF','IF','V')
  AND (name LIKE '%Aval%' OR name LIKE '%Asiento%' OR name LIKE '%XML%')
ORDER BY name;

SELECT name, state_desc FROM sys.databases WHERE state = 0;


SELECT referencing_schema_name, referencing_entity_name, referencing_class_desc
FROM sys.dm_sql_referencing_entities('dbo.archivoAsientoAval','OBJECT');

SELECT referencing_schema_name, referencing_entity_name
FROM sys.dm_sql_referencing_entities('dbo.tmp_repavalcierre','OBJECT');


SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_Genera_RepAval_cierre'));


SELECT TOP 50
       DB_NAME(t.dbid) AS db,
       qs.execution_count, qs.last_execution_time,
       LEFT(t.text, 1000) AS texto
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) t
WHERE t.text LIKE '%archivoAsientoAval%'
   OR t.text LIKE '%repavalcierre%'
ORDER BY qs.last_execution_time DESC;


SELECT user_seeks, user_scans, user_lookups, user_updates,
       last_user_seek, last_user_scan, last_user_lookup, last_user_update
FROM sys.dm_db_index_usage_stats
WHERE database_id = DB_ID() AND object_id = OBJECT_ID('dbo.archivoAsientoAval');


SELECT session_id, login_name, program_name, host_name,
       login_time, last_request_end_time, status
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
ORDER BY last_request_end_time DESC;

EXEC msdb.dbo.sp_help_job;

SELECT name FROM sys.databases WHERE name = 'SSISDB';
