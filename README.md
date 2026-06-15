SELECT @@SERVERNAME AS serverName, DB_NAME() AS databaseName;

SELECT COUNT(*) AS sourceRecords
FROM dbo.Datos_reporte_ext;

SELECT COUNT(*) AS generatedRecords
FROM dbo.reportecontable_peru;

SELECT COUNT(*) AS procedureResult
FROM dbo.Datos_reporte_ext d
LEFT JOIN dbo.Ramos_ext r
    ON r.codigoProdCardif = d.Codproducto;
