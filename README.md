SELECT COUNT(*) FROM CardifWP.dbo.tmpCargaSiniestrosAlfa;
SELECT NombreArchivo, COUNT(*) FROM CardifWP.dbo.CargaSiniestrosAlfa
GROUP BY NombreArchivo ORDER BY NombreArchivo;
