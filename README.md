SELECT name, base_object_name FROM sys.synonyms WHERE name = 'ha';
SELECT OBJECT_ID('dbo.ha') AS resuelve;          -- NULL = roto
SELECT name, data_source, provider FROM sys.servers;
SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_NAME = 'HistoricoasientosPru';       -- debe dar 27
