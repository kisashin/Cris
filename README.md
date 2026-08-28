USE [SiniestrosWp];
GO

DECLARE @corte datetime = DATEADD(DAY, -5, GETDATE());
DECLARE @llave nvarchar(510) = 'TEST-CARDIF-001';

DELETE FROM historicomovimientos WHERE archivocargue = 'PRUEBA_COL_CARDIF';
DELETE FROM historico_inicial WHERE Llavesiniestro = @llave;

INSERT INTO historico_inicial (
    IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion, Codproducto,
    CodPlan, Cobertura, Ramo, Llavesiniestro, Nombreasegurado, Aval)
VALUES (
    991000001, 'BANCOLOMBIA', '0902026A991001', '2030405060', '1895',
    '1', 'MUERTE ACCIDENTAL', '22', @llave, 'MARIA GOMEZ PRUEBA', 0);

SET IDENTITY_INSERT historicomovimientos ON;

INSERT INTO historicomovimientos (
    id, IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion,
    Codproducto, CodPlan, Cobertura, Ramo, Llavesiniestro,
    Nombreasegurado, Tipomovimiento, Vrmovimiento, Fechamovimiento2,
    Fechaocurrencia, Fechainiciovigencia, Certificado,
    Beneficiariopago, NumeroIdentificacionBeneficiarioDelPago,
    Iddoctosoportemanutencion, Fechacontabilizacion, marcaavalpos,
    tipocoaseguro, vrcoaseguroretenido,
    archivocargue, fechacargue)
VALUES
(991000001, 991000001, 'BANCOLOMBIA', '0902026A991001', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Reserva Inicial - Aseguradora', 2000000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 NULL, NULL, NULL, NULL, NULL,
 NULL, NULL, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000002, 991000002, 'BANCOLOMBIA', '0902026A991001', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Aumento Reserva', 600000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 NULL, NULL, NULL, NULL, NULL,
 NULL, NULL, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000003, 991000003, 'BANCOLOMBIA', '0902026A991001', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Pago', 900000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 'MARIA GOMEZ', '2030405060', 'PLANILLA-002', NULL, NULL,
 NULL, NULL, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000004, 991000004, 'BANCOLOMBIA', '0902026A991001', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Disminución Reserva', 400000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 NULL, NULL, NULL, NULL, NULL,
 NULL, NULL, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000005, 991000005, 'BANCOLOMBIA', '0902026A991001', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Reversa', 250000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 'MARIA GOMEZ', '2030405060', 'PLANILLA-002', NULL, NULL,
 NULL, NULL, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000006, 991000006, 'BANCOLOMBIA', '0902026A991002', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Reserva Inicial - Aseguradora', 1000000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 NULL, NULL, NULL, NULL, NULL,
 1, 600000.00, 'PRUEBA_COL_CARDIF', GETDATE()),

(991000007, 991000007, 'BANCOLOMBIA', '0902026A991002', '2030405060',
 '1895', '1', 'MUERTE ACCIDENTAL', '22', @llave,
 'MARIA GOMEZ PRUEBA', 'Pago', 700000.00, @corte,
 '20260101', '20250101', '7822434176267122',
 'MARIA GOMEZ', '2030405060', 'PLANILLA-002', NULL, NULL,
 1, 420000.00, 'PRUEBA_COL_CARDIF', GETDATE());

SET IDENTITY_INSERT historicomovimientos OFF;
GO





-- Debe dar 7
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 0)
  AND fechacontabilizacion IS NULL;

-- Debe dar 2 (los de coaseguro)
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 0)
  AND fechacontabilizacion IS NULL AND tipocoaseguro IS NOT NULL;

-- Debe dar 1
SELECT COUNT(*) FROM controlcierreaval;
