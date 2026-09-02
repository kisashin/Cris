{
  "message": "5 Registros Cargados : 326CO21SR0122026090110.csv",
  "totalRows": 5,
  "incompleteRows": 1
}


USE CardifWP;

SELECT NoRAMO, RAMO, SINIESTRO, ASEGURADO, AVISOS, PAGO_DEFINITIVO,
       LIBERACIONES_rebajas, TOMADOR, NombreArchivo, Producto
FROM CargaSiniestrosAlfa
WHERE NombreArchivo = '326CO21SR0122026090110.csv';


DELETE FROM CargaSiniestrosAlfa WHERE NombreArchivo = '326CO21SR0122026090110.csv';
DELETE FROM tmpCargaSiniestrosAlfa;
