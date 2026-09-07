USE CardifWP;

-- 1. Que la carga del archivo llegó
SELECT COUNT(*) AS filas_cargadas
FROM CargaSiniestrosAlfa
WHERE NombreArchivo = '326CO21SR0122026090701.csv';

SELECT TOP 5 NoRAMO, RAMO, SINIESTRO, ASEGURADO, TOMADOR,
       RES_ANTERIOR, AVISOS, PAGO_DEFINITIVO, LIBERACIONES_rebajas,
       NombreArchivo, Producto, FechaProceso
FROM CargaSiniestrosAlfa
WHERE NombreArchivo = '326CO21SR0122026090701.csv';

-- 2. Cuál es el último archivo que el SP va a tomar para el producto
SELECT TOP 1 NombreArchivo, FechaProceso, Producto
FROM CargaSiniestrosAlfa
WHERE Producto = 2012
ORDER BY FechaProceso DESC;

-- 3. Configuración que cruza sp_AsientoSiniestrosAdicionales modo 1
SELECT * FROM Socios_Prod_Siniestros WHERE producto = '2012';

SELECT producto, ramo, cobertura, peso, valor, afectadox
FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto = '2012';

SELECT tipodiario, ramo, cuenta, ref_transaccion, naturaleza
FROM Cuentas_Contables_Prod_Siniestros
WHERE tipodiario IN ('LRVSI','CRVSI','SINIE')
ORDER BY tipodiario, ramo;

-- 4. El cruce completo: si esto da 0, ahí está la causa
SELECT COUNT(*) AS filas_del_join
FROM dbo.CargaSiniestrosAlfa sini
INNER JOIN dbo.Socios_Prod_Siniestros so ON so.producto = '2012'
INNER JOIN dbo.Cobertura_Prod_Xpln_Plz_Cnl co ON co.producto = '2012'
INNER JOIN Cuentas_Contables_Prod_Siniestros cu ON cu.tipodiario IN ('LRVSI','CRVSI','SINIE')
WHERE sini.producto = 2012
  AND co.ramo = cu.ramo
  AND sini.NombreArchivo = '326CO21SR0122026090701.csv';

-- 5. Patrones y layout de los cinco productos activos
SELECT producto, patron, layout
FROM PatronxProd_siniestros
WHERE producto IN (2011,2012,2014,2020,2028)
ORDER BY producto;

-- 6. Periodo contable configurado en TEST
SELECT id, periodocontable,
       dbo.fFecha2Txt(periodocontable,'') AS fecha_txt,
       dbo.fFecha2Txt(periodocontable,'/') AS fecha_periodo
FROM parametro WHERE id = 4;

-- 7. Estado de la tabla nueva
SELECT COUNT(*) AS archivos_generados FROM archivoAsientoReaseguro;

-- 8. Movimientos existentes en el periodo, por si hay datos previos
SELECT producto, periodo_contable, descripcion_asiento, tipo_diario, estado, COUNT(*) AS movimientos
FROM HistoricoAsientosPru
WHERE tipo_diario IN ('SINIE','LRVSI','CRVSI')
GROUP BY producto, periodo_contable, descripcion_asiento, tipo_diario, estado
ORDER BY periodo_contable DESC, producto;

-- 9. Que los sinónimos resuelvan bien en TEST
SELECT name, base_object_name FROM sys.synonyms;

-- 10. Comparación de configuración entre productos, por si 2012 es el único sin datos
SELECT producto, COUNT(*) AS coberturas
FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028')
GROUP BY producto;

SELECT producto, COUNT(*) AS socios
FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028')
GROUP BY producto;
