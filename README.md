SELECT OBJECT_ID('dbo.HistoricoAsientosPru') AS tabla_local;

DROP SYNONYM dbo.ha;
CREATE SYNONYM dbo.ha FOR [CardifWP].[dbo].[HistoricoasientosPru];
