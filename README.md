SELECT name, base_object_name FROM sys.synonyms;

SELECT OBJECT_NAME(object_id) AS objeto
FROM sys.sql_modules
WHERE definition LIKE '%BOGS005DVSQL01%';

SELECT name, product, data_source FROM sys.servers;

SELECT name, type_desc FROM sys.objects
WHERE name IN ('ha','CargaSiniestrosAlfa','Socios_Prod_Siniestros',
               'Cobertura_Prod_Xpln_Plz_Cnl','Cuentas_Contables_Prod_Siniestros',
               'HistoricoAsientosPru');

SELECT TOP 20 Descripcion_Asiento, Periodo_Contable, Tipo_Diario, COUNT(*) AS filas
FROM HistoricoAsientosPru
GROUP BY Descripcion_Asiento, Periodo_Contable, Tipo_Diario
ORDER BY Descripcion_Asiento;

SELECT * FROM UsuariosCierre;




USE CardifWP;

SELECT name, base_object_name FROM sys.synonyms;

SELECT OBJECT_NAME(object_id) AS objeto
FROM sys.sql_modules
WHERE definition LIKE '%BOGS005DVSQL01%';

SELECT name, product, data_source FROM sys.servers;


USE SiniestrosWp;

SELECT name, base_object_name FROM sys.synonyms;

SELECT OBJECT_NAME(object_id) AS objeto
FROM sys.sql_modules
WHERE definition LIKE '%BOGS005DVSQL01%';
