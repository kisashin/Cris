USE SiniestrosWp;

SELECT COUNT(*) AS filas, COUNT(DISTINCT id) AS ids_distintos
FROM historicomovimientos;

SELECT n.codigo, n.Id, COUNT(h.IDCARVAJAL) AS coincidencias
FROM novedadhistoricoindividual n
LEFT JOIN historicomovimientos h ON h.id = n.Id
GROUP BY n.codigo, n.Id;

SELECT fk.name, OBJECT_NAME(fk.parent_object_id) AS tabla,
       OBJECT_NAME(fk.referenced_object_id) AS referencia
FROM sys.foreign_keys fk
WHERE fk.parent_object_id = OBJECT_ID('novedadhistoricoindividual');
