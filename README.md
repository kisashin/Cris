SELECT session_id, status, command, wait_type, wait_time, blocking_session_id
FROM sys.dm_exec_requests
WHERE session_id > 50;

SELECT DISTINCT estado FROM ha WHERE descripcion_asiento = '2012_202602';

EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\*2012*.XML';


SELECT * FROM UsuariosCierre;
