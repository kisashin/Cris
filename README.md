,replace(convert(varchar(30),cast(A.Valordeuda as DECIMAL(18,2))),'.',',') as Valordeuda  
,replace(convert(varchar(30),cast(A.Valoraseguradototal as DECIMAL(18,2))),'.',',') as Valoraseguradototal

,replace(convert(varchar(30),cast(A.vrReaseguroRetenido as DECIMAL(18,2))),'.',',') as vrReaseguroRetenido  
,replace(convert(varchar(30),cast(A.vrReaseguroCedido as DECIMAL(18,2))),'.',',') as vrReaseguroCedido
