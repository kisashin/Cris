USE [SiniestrosWp];
GO

DECLARE @corte datetime = DATEADD(DAY, -5, GETDATE());
DECLARE @llave nvarchar(510) = 'TEST-AVAL-001';

DELETE FROM historicomovimientos WHERE archivocargue = 'PRUEBA_COL_AVAL';
DELETE FROM historico_inicial WHERE Llavesiniestro = @llave;

INSERT INTO historico_inicial (
    IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion, Codproducto,
    CodPlan, Cobertura, Ramo, Llavesiniestro, Nombreasegurado, Aval)
VALUES (
    990000001, 'BANCO DE BOGOTA', '0902026A990001', '1020304050', '763',
    '1', 'MUERTE ACCIDENTAL', '7', @llave, 'JUAN PEREZ PRUEBA', 1);

SET IDENTITY_INSERT historicomovimientos ON;

INSERT INTO historicomovimientos (
    id, IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion,
    Codproducto, CodPlan, Cobertura, Ramo, Llavesiniestro,
    Nombreasegurado, Tipomovimiento, Vrmovimiento, Fechamovimiento2,
    Fechaocurrencia, Fechainiciovigencia, Certificado,
    Beneficiariopago, NumeroIdentificacionBeneficiarioDelPago,
    Iddoctosoportemanutencion, Fechacontabilizacion, marcaavalpos,
    archivocargue, fechacargue)
VALUES
(990000001, 990000001, 'BANCO DE BOGOTA', '0902026A990001', '1020304050',
 '763', '1', 'MUERTE ACCIDENTAL', '7', @llave,
 'JUAN PEREZ PRUEBA', 'Reserva Inicial - Re-Aseguradora', 1500000.00, @corte,
 '20260101', '20250101', '6722434176267121',
 NULL, NULL, NULL, NULL, NULL, 'PRUEBA_COL_AVAL', GETDATE()),

(990000002, 990000002, 'BANCO DE BOGOTA', '0902026A990001', '1020304050',
 '763', '1', 'MUERTE ACCIDENTAL', '7', @llave,
 'JUAN PEREZ PRUEBA', 'Aumento Reserva', 500000.00, @corte,
 '20260101', '20250101', '6722434176267121',
 NULL, NULL, NULL, NULL, NULL, 'PRUEBA_COL_AVAL', GETDATE()),

(990000003, 990000003, 'BANCO DE BOGOTA', '0902026A990001', '1020304050',
 '763', '1', 'MUERTE ACCIDENTAL', '7', @llave,
 'JUAN PEREZ PRUEBA', 'Pago', 800000.00, @corte,
 '20260101', '20250101', '6722434176267121',
 'BANCO DE BOGOTA', '8600029644', 'PLANILLA-001',
 NULL, NULL, 'PRUEBA_COL_AVAL', GETDATE()),

(990000004, 990000004, 'BANCO DE BOGOTA', '0902026A990001', '1020304050',
 '763', '1', 'MUERTE ACCIDENTAL', '7', @llave,
 'JUAN PEREZ PRUEBA', 'Disminución Reserva', 300000.00, @corte,
 '20260101', '20250101', '6722434176267121',
 NULL, NULL, NULL, NULL, NULL, 'PRUEBA_COL_AVAL', GETDATE()),

(990000005, 990000005, 'BANCO DE BOGOTA', '0902026A990001', '1020304050',
 '763', '1', 'MUERTE ACCIDENTAL', '7', @llave,
 'JUAN PEREZ PRUEBA', 'Reversa', 200000.00, @corte,
 '20260101', '20250101', '6722434176267121',
 'BANCO DE BOGOTA', '8600029644', 'PLANILLA-001',
 NULL, NULL, 'PRUEBA_COL_AVAL', GETDATE());

SET IDENTITY_INSERT historicomovimientos OFF;
GO






-- Debe dar 5
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);

-- Debe dar 5 tambien
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 1)
  AND fechacontabilizacion IS NULL AND marcaavalpos IS NULL;

-- Confirmar que el producto no esta excluido
SELECT * FROM dbo.productosnoaval WHERE producto = '763';



UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue = 'PRUEBA_COL_AVAL';

DELETE FROM controlcierreaval;
DELETE FROM archivoAsientoAvalXml;
