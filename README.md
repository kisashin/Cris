SELECT c.name, c.is_identity
FROM sys.columns c
WHERE c.object_id = OBJECT_ID('dbo.tmp_repavalcierre')
  AND c.name = 'id';
