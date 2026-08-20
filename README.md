SELECT Identificacion, Nombre, Estado, Fecha, Proceso
FROM dbo.historicoterceros WITH (NOLOCK)
WHERE Identificacion IN ('47031846','48267407','70882062','16166025','30677354')
ORDER BY Identificacion, Nombre;
