SELECT DISTINCT archivocargue, marcaavalpos, COUNT(*)
FROM historicomovimientos
WHERE marcaavalpos IS NOT NULL
GROUP BY archivocargue, marcaavalpos;
