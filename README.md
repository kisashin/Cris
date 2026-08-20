SELECT '[' + name + ']' AS exacto, DATALENGTH(name)/2 AS largo, column_id
FROM sys.columns WHERE object_id = OBJECT_ID('dbo.historicoterceros')
ORDER BY column_id;

SELECT * FROM dbo.historicoterceros WITH (NOLOCK)
WHERE Identificacion IN ('47031846','48267407','70882062','16166025','30677354')
ORDER BY Identificacion;
