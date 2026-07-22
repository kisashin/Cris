SELECT COUNT(*) AS total_sesiones_abiertas
FROM sys.dm_exec_sessions
WHERE is_user_process = 1;

SELECT
    session_id,
    login_name,
    host_name,
    program_name,
    status,
    login_time,
    last_request_start_time,
    last_request_end_time
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
ORDER BY session_id;
