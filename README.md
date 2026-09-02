USE CardifWP;
SELECT t.name AS trigger_name, OBJECT_NAME(t.parent_id) AS tabla, t.is_disabled
FROM sys.triggers t
WHERE OBJECT_NAME(t.parent_id) = 'tmpdesc';
