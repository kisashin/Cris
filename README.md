SELECT 
    db_name(dbid) AS base_conectada,
    loginame,
    hostname,
    program_name,
    login_time,
    last_batch
FROM sys.sysprocesses
WHERE dbid > 4                    -- excluye master, tempdb, model, msdb
  AND loginame <> ''
ORDER BY last_batch DESC;
