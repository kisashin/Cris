SELECT c.name, t.name AS tipo, c.max_length, c.precision, c.scale
FROM cardifwp.sys.columns c
JOIN cardifwp.sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = (SELECT object_id FROM cardifwp.sys.objects
                     WHERE name = 'CUENTAS_CONTABLES_PROD' AND type = 'U')
ORDER BY c.column_id;
