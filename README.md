SELECT 'SiniestrosWp' AS BD,
       OBJECT_ID('SiniestrosWp.dbo.historicomovimientos')      AS historicomovimientos,
       OBJECT_ID('SiniestrosWp.dbo.novedadhistoricoindividual') AS novedades
UNION ALL
SELECT 'CardifWP',
       OBJECT_ID('CardifWP.dbo.historicomovimientos'),
       OBJECT_ID('CardifWP.dbo.novedadhistoricoindividual');
