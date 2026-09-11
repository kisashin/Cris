USE [SiniestrosWp];
GO

DELETE FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 07 09 2026.xlsx';

DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
GO

INSERT INTO historico_inicial (
    IDCARVAJAL, Socio, NumeroSiniestro, Nroidentificacion, Codproducto,
    CodPlan, Cobertura, Ramo, Llavesiniestro, Nombreasegurado, Aval)
SELECT DISTINCT
    hm.IDCARVAJAL, hm.Socio, hm.NumeroSiniestro, hm.Nroidentificacion,
    hm.Codproducto, hm.CodPlan, hm.Cobertura, hm.Ramo,
    hm.Llavesiniestro, hm.Nombreasegurado,
    CASE WHEN hm.Socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS',
                           'BANCO DE OCCIDENTE','BANCO POPULAR')
         THEN 1 ELSE 0 END
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Llavesiniestro IS NULL;

SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
