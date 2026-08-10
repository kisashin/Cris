DELETE FROM dbo.tbl_Archivo_socios
WHERE idArchivosocios_cen IN (2, 3);

INSERT INTO dbo.tbl_Archivo_socios (nombredatos, nombremov, fechaproceso, estado, id)
VALUES ('', '', GETDATE(), 'PENDIENTE', 1),
       ('', '', GETDATE(), 'PENDIENTE', 1);
