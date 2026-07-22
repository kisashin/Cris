SELECT s.name, s.base_object_name,
       OBJECTPROPERTYEX(s.object_id, 'BaseType') AS tipo_destino  -- NULL = no resuelve
FROM sys.synonyms s WHERE s.name = 'ha';

SELECT * FROM dbo.ha WHERE 1 = 0;   -- si truena, está roto

SELECT server_id, name, is_linked, data_source FROM sys.servers;
SELECT @@SERVERNAME, SERVERPROPERTY('MachineName');


SELECT dp.permission_name, dp.state_desc, pr.name AS principal
FROM sys.database_permissions dp
JOIN sys.database_principals pr ON pr.principal_id = dp.grantee_principal_id
WHERE dp.major_id = OBJECT_ID('dbo.ha');


SELECT name, base_object_name FROM sys.synonyms
WHERE base_object_name LIKE '%DVSQL01%' OR base_object_name LIKE '%[[]%[]].[[]%';


SELECT COUNT(*) AS filas, MAX(fecha_proceso) AS ultimo
FROM CardifWP.dbo.HistoricoasientosPru;

SELECT producto, periodo_contable, estado, COUNT(*)
FROM CardifWP.dbo.HistoricoasientosPru
WHERE producto = '2012'
GROUP BY producto, periodo_contable, estado;
