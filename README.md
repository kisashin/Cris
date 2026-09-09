EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_ReasegAlfa';
EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_ReasegCardif';
EXEC sp_helptext 'dbo.sp_Gen_Xml_Siniestros_CoaseguroC';
EXEC sp_helptext 'dbo.sp_XMLAsientosPru';
EXEC sp_helptext 'dbo.sp_contabiliza_aval';
EXEC sp_helptext 'dbo.sp_contabiliza_cardif';
EXEC sp_helptext 'dbo.sp_contabiliza_coaseguro';


SELECT id, TIPODIARIO, CUENTA, NATURALEZA, REF_TRANSACCION, Formula, 
       Observacion, ramo, GRUPO, Iva
FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO IN ('HOGAR','RSGCAR','CC')
ORDER BY GRUPO, left(Observacion,1), TIPODIARIO, id;

SELECT * FROM cardifwp.dbo.x100_Hogar_Otros_Cierre;

SELECT * FROM cardifwp.dbo.Ramos_Cierre WHERE Origen = 'CO';

SELECT * FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
WHERE GRUPO IN ('A','C');
