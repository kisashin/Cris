SELECT COUNT(*) FROM dbo.historicomovimientos_ext WITH (NOLOCK)
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial_ext);



  SELECT COUNT(*) INTO #antes FROM dbo.historicomovimientos_ext WHERE fechacontabilizacion IS NULL;

UPDATE dbo.historicomovimientos_ext
SET fechacontabilizacion = dbo.truncdate(getdate())
WHERE fechacontabilizacion IS NULL;

SELECT COUNT(*) AS restantes FROM dbo.historicomovimientos_ext WHERE fechacontabilizacion IS NULL;


UPDATE dbo.historicoterceros SET estado = 1, fechaimpreso = GETDATE()
WHERE estado = 0 AND proceso = 'PERU';


INSERT INTO dbo.historicomovimientos_ext (
    Socio, NumeroSiniestro, Nroidentificacion, Tipodocumento, Nombreasegurado,
    Codproducto, CodPlan, Cobertura, Ramo, Fechamovimiento2, Vrmovimiento,
    Tipomovimiento, Llavesiniestro, vrReaseguroRetenido, Moneda,
    Fechacontabilizacion, Fechaavisocardif
)
SELECT TOP 10
    Socio, 'TEST' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY id) AS varchar), 3),
    Nroidentificacion, Tipodocumento, Nombreasegurado,
    Codproducto, CodPlan, Cobertura, Ramo,
    '2026-08-15', 1000000,
    'Reserva Inicial - Aseguradora',
    'TESTKEY' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY id) AS varchar), 3),
    '200000', Moneda,
    NULL, '2026-08-15'
FROM dbo.historicomovimientos_ext
WHERE Codproducto IS NOT NULL AND Ramo IS NOT NULL AND Moneda IS NOT NULL;


INSERT INTO dbo.historico_inicial_ext (llavesiniestro)
SELECT DISTINCT Llavesiniestro FROM dbo.historicomovimientos_ext
WHERE Llavesiniestro LIKE 'TESTKEY%';


SELECT COUNT(*) FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD WHERE GRUPO='RE';
SELECT COUNT(*) FROM cardifwp.dbo.Ramos_Cierre WHERE Origen='CO';


//////////////////////////


SELECT '[' + c.name + ']' AS columna, t.name AS tipo,
       CASE WHEN t.name LIKE 'n[cv]%' THEN c.max_length/2 ELSE c.max_length END AS largo,
       c.is_nullable, c.is_identity, c.column_id
FROM sys.columns c
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.historico_inicial_ext')
ORDER BY c.column_id;

SELECT TOP 3 * FROM dbo.historico_inicial_ext WITH (NOLOCK);

-- Sin esto, ##xmlSin queda vacío y no se genera ningún XML
SELECT COUNT(*) AS cuentas FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD WHERE GRUPO='RE' AND TIPODIARIO IN ('CRVSI','LRVSI','SINIE');
SELECT COUNT(*) AS ramos FROM cardifwp.dbo.Ramos_Cierre WHERE Origen='CO';

-- Los ramos que existen, para elegir uno válido en el poblado
SELECT DISTINCT ramo, iva FROM cardifwp.dbo.Ramos_Cierre WHERE Origen='CO' ORDER BY ramo;

-- Verifica que las coberturas que vas a clonar caben en 50
SELECT COUNT(*) FROM dbo.historicomovimientos_ext WITH (NOLOCK) WHERE LEN(Cobertura) > 50;
