SELECT
    'NumeroSiniestro + Fechamovimiento2' AS candidateKey,
    (
        SELECT COUNT(*)
        FROM dbo.reportecontable_peru
        WHERE NumeroSiniestro IS NULL
           OR Fechamovimiento2 IS NULL
    ) AS rowsWithNulls,
    (
        SELECT COUNT(*)
        FROM (
            SELECT NumeroSiniestro, Fechamovimiento2
            FROM dbo.reportecontable_peru
            GROUP BY NumeroSiniestro, Fechamovimiento2
            HAVING COUNT(*) > 1
        ) duplicates
    ) AS duplicateGroups

UNION ALL

SELECT
    'NumeroSiniestro + CoberturaAfectada',
    (
        SELECT COUNT(*)
        FROM dbo.reportecontable_peru
        WHERE NumeroSiniestro IS NULL
           OR CoberturaAfectada IS NULL
    ),
    (
        SELECT COUNT(*)
        FROM (
            SELECT NumeroSiniestro, CoberturaAfectada
            FROM dbo.reportecontable_peru
            GROUP BY NumeroSiniestro, CoberturaAfectada
            HAVING COUNT(*) > 1
        ) duplicates
    )

UNION ALL

SELECT
    'NumeroSiniestro + Certificado',
    (
        SELECT COUNT(*)
        FROM dbo.reportecontable_peru
        WHERE NumeroSiniestro IS NULL
           OR Certificado IS NULL
    ),
    (
        SELECT COUNT(*)
        FROM (
            SELECT NumeroSiniestro, Certificado
            FROM dbo.reportecontable_peru
            GROUP BY NumeroSiniestro, Certificado
            HAVING COUNT(*) > 1
        ) duplicates
    )

UNION ALL

SELECT
    'NumeroSiniestro + FechaRegTransaccion',
    (
        SELECT COUNT(*)
        FROM dbo.reportecontable_peru
        WHERE NumeroSiniestro IS NULL
           OR FechaRegTransaccion IS NULL
    ),
    (
        SELECT COUNT(*)
        FROM (
            SELECT NumeroSiniestro, FechaRegTransaccion
            FROM dbo.reportecontable_peru
            GROUP BY NumeroSiniestro, FechaRegTransaccion
            HAVING COUNT(*) > 1
        ) duplicates
    );
