SELECT s.session_id, s.login_name, s.status, r.command, r.wait_type,
       r.blocking_session_id, t.transaction_id
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r ON r.session_id = s.session_id
LEFT JOIN sys.dm_tran_session_transactions t ON t.session_id = s.session_id
WHERE s.is_user_process = 1;

SELECT ORDINAL_POSITION, COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tmpAR';
