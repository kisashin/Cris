SELECT ORDINAL_POSITION, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'tmpAR'
ORDER BY ORDINAL_POSITION;


SELECT s.session_id, s.login_name, s.status, s.last_request_end_time
FROM sys.dm_tran_session_transactions t
JOIN sys.dm_exec_sessions s ON s.session_id = t.session_id;


EXEC dbo.sp_AsientoSiniestrosAdicionales 2, '2012_202602', '2012';
