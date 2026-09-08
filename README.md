USE [SiniestrosWp];
GO

-- Tablas nuevas: CRUD completo
GRANT SELECT, INSERT, UPDATE, DELETE ON dbo.archivoAsientoAvalXml TO [USUARIO_APP];
GRANT SELECT, INSERT, UPDATE, DELETE ON dbo.archivoAsientoCardifXml TO [USUARIO_APP];

-- Procedimientos orquestadores
GRANT EXECUTE ON dbo.sp_contabiliza_aval TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_contabiliza_cardif TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_contabiliza_coaseguro TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_Genera_RepAval_cierre TO [USUARIO_APP];

-- Procedimientos generadores
GRANT EXECUTE ON dbo.sp_XMLAsientosPru TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_Gen_Xml_Siniestros_ReasegAlfa TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_Gen_Xml_Siniestros_ReasegCardif TO [USUARIO_APP];
GRANT EXECUTE ON dbo.sp_Gen_Xml_Siniestros_CoaseguroC TO [USUARIO_APP];

-- Procedimiento invocado por los orquestadores
GRANT EXECUTE ON dbo.sp_asientosSiniestros TO [USUARIO_APP];
GO
