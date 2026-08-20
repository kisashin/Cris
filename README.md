SELECT s.session_id, s.login_name, s.host_name, s.program_name,
       r.blocking_session_id, r.wait_type, r.wait_time/1000 AS seg,
       t.text
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r ON r.session_id = s.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE s.is_user_process = 1
  AND (r.blocking_session_id > 0 OR s.session_id IN
       (SELECT blocking_session_id FROM sys.dm_exec_requests WHERE blocking_session_id > 0));

       
