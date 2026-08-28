inner join cardifwp.[dbo].[CUENTAS_CONTABLES_PROD] c on c.GRUPO='CC'
where c.TIPODIARIO in('CRVSI','LRVSI','SINIE')
AND ((c.IVA='SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre where iva<>0 and Origen='CO'))
  or (c.IVA<>'SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre where iva=0 and Origen='CO')))






  SELECT ramo, iva, Origen 
FROM cardifwp.dbo.Ramos_Cierre 
WHERE Origen = 'CO' AND ramo = 22;

SELECT COUNT(*) FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD WHERE GRUPO = 'CC';

SELECT DISTINCT ramo, iva FROM cardifwp.dbo.Ramos_Cierre WHERE Origen = 'CO';
