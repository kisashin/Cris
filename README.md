SELECT HAS_PERMS_BY_NAME(NULL, NULL, 'VIEW SERVER STATE') AS puedo_ver;


DBCC INPUTBUFFER(71);
SELECT resource_type, resource_associated_entity_id, request_mode, request_status
FROM sys.dm_tran_locks WHERE request_session_id = 71;

DBCC SQLPERF(LOGSPACE);

KILL 71;
KILL 71 WITH STATUSONLY;   -- repite hasta que diga que no hay rollback pendiente
DBCC OPENTRAN('CardifWP'); -- debe decir "No active open transactions"

USE CardifWP;
GO
DROP SYNONYM dbo.ha;
CREATE SYNONYM dbo.ha FOR [dbo].[HistoricoasientosPru];
GO
SELECT name, base_object_name, OBJECTPROPERTYEX(object_id,'BaseType') AS resuelve
FROM sys.synonyms WHERE name = 'ha';   -- tiene que decir 'U '


SELECT s.name AS sinonimo, dp.permission_name, dp.state_desc, pr.name AS principal
FROM sys.synonyms s
LEFT JOIN sys.database_permissions dp ON dp.major_id = s.object_id
LEFT JOIN sys.database_principals pr ON pr.principal_id = dp.grantee_principal_id
ORDER BY s.name;
