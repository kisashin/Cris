SELECT COUNT(*) AS antes FROM dbo.historicomovimientos_ext WHERE fechacontabilizacion IS NULL;

UPDATE dbo.historicomovimientos_ext
SET fechacontabilizacion = dbo.truncdate(getdate())
WHERE fechacontabilizacion IS NULL;

UPDATE dbo.historicoterceros
SET estado = 1, fechaimpreso = GETDATE()
WHERE estado = 0 AND proceso = 'PERU';

SELECT COUNT(*) AS restantes FROM dbo.historicomovimientos_ext WHERE fechacontabilizacion IS NULL;

INSERT INTO dbo.historicomovimientos_ext (
    IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion, Tipodocumento,
    Nombreasegurado, Codproducto, CodPlan, Cobertura, Ramo,
    Fechamovimiento2, Fechaavisocardif, Vrmovimiento, Tipomovimiento,
    Llavesiniestro, vrReaseguroRetenido, Moneda,
    Fechacontabilizacion, marcaavalpos
)
SELECT TOP 10
    999000000000 + ROW_NUMBER() OVER (ORDER BY IDCARVAJAL),
    Socio,
    'TEST' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY IDCARVAJAL) AS varchar), 3),
    Nroidentificacion, Tipodocumento, Nombreasegurado,
    Codproducto, '1', Cobertura, '9',
    '2026-08-15', '2026-08-15', 1000000,
    'Reserva Inicial - Aseguradora',
    'TESTKEY' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY IDCARVAJAL) AS varchar), 3),
    200000, 'PEN',
    NULL, NULL
FROM dbo.historicomovimientos_ext WITH (NOLOCK)
WHERE Codproducto IS NOT NULL
  AND Moneda IS NOT NULL
  AND LEN(Cobertura) <= 50;

  INSERT INTO dbo.historico_inicial_ext (IDCARVAJAL, Llavesiniestro, NumeroSiniestro)
SELECT IDCARVAJAL, Llavesiniestro, NumeroSiniestro
FROM dbo.historicomovimientos_ext WITH (NOLOCK)
WHERE Llavesiniestro LIKE 'TESTKEY%';

SELECT COUNT(*) AS listos FROM dbo.historicomovimientos_ext
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial_ext);
