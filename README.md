SELECT
    h.id_historico_movimiento,
    h.NumeroSiniestro,
    h.Llavesiniestro,
    h.TipoMovimiento,
    h.Fechamovimiento2,
    h.Fechacontabilizacion,
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM dbo.TBL_historico_inicial i
            WHERE i.llavesiniestro = h.llavesiniestro
        )
        THEN 'SI_EXISTE_EN_TBL_HISTORICO_INICIAL'
        ELSE 'NO_EXISTE_EN_TBL_HISTORICO_INICIAL'
    END AS validacion_inicial
FROM dbo.TBL_Historico_Movimientos h
WHERE h.id_historico_movimiento = 20012399;


SELECT
    h.id_historico_movimiento,
    '[' + h.llavesiniestro + ']' AS llave_historico,
    LEN(h.llavesiniestro) AS len_historico
FROM dbo.TBL_Historico_Movimientos h
WHERE h.id_historico_movimiento = 20012399;


SELECT
    '[' + i.llavesiniestro + ']' AS llave_inicial,
    LEN(i.llavesiniestro) AS len_inicial
FROM dbo.TBL_historico_inicial i
WHERE i.llavesiniestro LIKE '%90044737217162A162-DESEMPLEO%';
