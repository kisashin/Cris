SELECT '[' + name + ']' AS exacto, DATALENGTH(name)/2 AS largo_real,
       TYPE_NAME(system_type_id) AS tipo, max_length/2 AS ancho
FROM sys.columns WHERE object_id = OBJECT_ID('dbo.vw_mov_cardif_ext')
ORDER BY column_id;
