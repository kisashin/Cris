USE CardifWP;
GO
SELECT DB_NAME() AS bd, name, base_object_name,
       OBJECTPROPERTYEX(object_id, 'BaseType') AS resuelve
FROM sys.synonyms WHERE name = 'ha';

SELECT 'master' AS bd, name, base_object_name FROM master.sys.synonyms WHERE name='ha';


SELECT COUNT(*) FROM CardifWP.dbo.HistoricoasientosPru WITH (NOLOCK);

SELECT r.session_id, r.blocking_session_id, r.status, r.command,
       r.wait_type, r.wait_time, s.login_name, s.host_name, s.program_name
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON s.session_id = r.session_id
WHERE r.blocking_session_id <> 0;

SELECT s.session_id, s.login_name, s.host_name, s.program_name,
       s.open_transaction_count, s.last_request_start_time, s.last_request_end_time
FROM sys.dm_exec_sessions s
WHERE s.open_transaction_count > 0;

DBCC OPENTRAN('CardifWP');


SELECT s.name AS sinonimo, dp.permission_name, dp.state_desc, pr.name AS principal
FROM sys.synonyms s
LEFT JOIN sys.database_permissions dp ON dp.major_id = s.object_id
LEFT JOIN sys.database_principals pr ON pr.principal_id = dp.grantee_principal_id
ORDER BY s.name;
