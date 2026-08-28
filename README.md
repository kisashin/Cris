USE [SiniestrosWp];
GO

DECLARE @corte datetime = DATEADD(DAY, -5, GETDATE());
DECLARE @llave nvarchar(510) = 'TEST-COASEG-001';

DELETE FROM historicomovimientos WHERE archivocargue = 'PRUEBA_COL_COASEG';
DELETE FROM historico_inicial WHERE Llavesiniestro = @llave;

INSERT INTO historico_inicial (
    IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion, Codproducto,
    CodPlan, Cobertura, Ramo, Llavesiniestro, Nombreasegurado, Aval)
VALUES (
    992000001, 'BANCOLOMBIA', '0902026A992001', '3040506070', '1895',
    '1', 'HURTO', '9', @llave, 'CARLOS RUIZ PRUEBA', 0);

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
(992000001, 992000001, 'BANCOLOMBIA', '0902026A992001', '3040506070',
 '1895', '1', 'HURTO', '9', @llave,
 'CARLOS RUIZ PRUEBA', 'Reserva Inicial - Aseguradora', 1000000.00, @corte,
 '20260101', '20250101', '9922434176267133',
 NULL, NULL, NULL, NULL, NULL,
 1, 600000.00, 'PRUEBA_COL_COASEG', GETDATE()),

(992000002, 992000002, 'BANCOLOMBIA', '0902026A992001', '3040506070',
 '1895', '1', 'HURTO', '9', @llave,
 'CARLOS RUIZ PRUEBA', 'Pago', 700000.00, @corte,
 '20260101', '20250101', '9922434176267133',
 'CARLOS RUIZ', '3040506070', 'PLANILLA-003', NULL, NULL,
 1, 420000.00, 'PRUEBA_COL_COASEG', GETDATE()),

(992000003, 992000003, 'BANCOLOMBIA', '0902026A992001', '3040506070',
 '1895', '1', 'HURTO', '9', @llave,
 'CARLOS RUIZ PRUEBA', 'Disminución Reserva', 300000.00, @corte,
 '20260101', '20250101', '9922434176267133',
 NULL, NULL, NULL, NULL, NULL,
 1, 180000.00, 'PRUEBA_COL_COASEG', GETDATE());

SET IDENTITY_INSERT historicomovimientos OFF;
GO



UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue IN ('PRUEBA_COL_CARDIF', 'PRUEBA_COL_COASEG');

DELETE FROM controlcierreaval;
INSERT INTO controlcierreaval VALUES (1, GETDATE());

DELETE FROM archivoAsientoCardifXml;




-- Debe dar 3
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 0)
  AND fechacontabilizacion IS NULL AND tipocoaseguro IS NOT NULL;
