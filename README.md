SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'HistoricoAsientosPru' ORDER BY ORDINAL_POSITION;



USE CardifWP;
BEGIN TRANSACTION;

INSERT INTO HistoricoAsientosPru
SELECT TOP 6
       Tipo_Diario, Periodo_Contable, Fecha_Transaccion, Codigo_Cuenta,
       Ref_Transaccion, Descripcion, Fecha_Vencimiento, Codigo_Moneda,
       Importe_Transaccion, Importe_Base, Debito_Credito, Centro_Costos,
       '2014' AS Producto,
       Ramo, Impuestos, Socio, NIT_Cedula, Clave_Asesor, Cobertura,
       X_Definir, IdPlan, Origen_Diario, Formato, Fecha_Proceso,
       '2014_202602' AS Descripcion_Asiento,
       'Pendiente XML' AS Estado,
       NoSiniestro
FROM HistoricoAsientosPru
WHERE producto = '2012'
  AND periodo_contable = '2026/002'
  AND tipo_diario = 'SINIE';

SELECT producto, tipo_diario, estado, COUNT(*)
FROM HistoricoAsientosPru
WHERE producto = '2014' AND periodo_contable = '2026/002'
GROUP BY producto, tipo_diario, estado;

-- Si el conteo se ve bien:
COMMIT;
-- Si algo salió mal:
-- ROLLBACK;


DELETE FROM HistoricoAsientosPru
WHERE producto = '2014' AND periodo_contable = '2026/002'
  AND descripcion_asiento = '2014_202602';

DELETE FROM archivoAsientoReaseguro WHERE producto = '2014';
