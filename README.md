SELECT convert(nvarchar(6), Fechamovimiento2, 112) AS periodo, COUNT(*)
FROM dbo.historicomovimientos_ext WITH (NOLOCK)
WHERE fechacontabilizacion IS NULL
GROUP BY convert(nvarchar(6), Fechamovimiento2, 112)
ORDER BY 1 DESC;
