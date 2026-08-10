SELECT idArchivosocios_cen, nombredatos, nombremov, fechaproceso, estado, id
FROM dbo.tbl_Archivo_socios
WHERE id = 1;

SELECT
    fk.name,
    OBJECT_NAME(fk.parent_object_id) AS tabla_hija
FROM sys.foreign_keys fk
WHERE fk.referenced_object_id = OBJECT_ID('dbo.tbl_Archivo_socios');
