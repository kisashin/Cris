USE CardifWP;

-- 1. Que se persistieron los archivos
SELECT id, producto, tipoDiario, periodoContable, nombreArchivo,
       LEN(contenido) AS largo, fechaGeneracion, usuario
FROM archivoAsientoReaseguro
ORDER BY producto, tipoDiario;

-- 2. Que el estado quedó marcado
SELECT tipo_diario, estado, COUNT(*)
FROM HistoricoAsientosPru
WHERE producto = '2012' AND periodo_contable = '2026/002'
  AND descripcion_asiento = '2012_202602'
GROUP BY tipo_diario, estado;
