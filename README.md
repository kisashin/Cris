Begin  
 if @varxml is not null and @XmlDestino <> 'PANTALLA'
 begin  
  drop table if exists ##VARXML

  exec xp_cmdshell 'net use t: /delete',no_output;  
 end;  
end;  

if @XmlDestino = 'PANTALLA'
begin
 select @Tipo_Diario Tipo_Diario,
        @ar NombreArchivo,
        case when @varxml is null then null
             else '<?xml version="1.0" encoding="UTF-8" ?>' + @varxml
        end Contenido;
 return 0;
end;

select @Tipo_Diario Tipo_Diario ,@ar ar,@Periodo_Contable Periodo_Contable,@Producto Producto, @ajuste ajuste, @XmlDestino XmlDestino  
if @varxml is  null select '0';  
END;


-- modo legacy: debe comportarse como hoy
EXEC dbo.sp_XMLAsientosPru 'SINIE', '2026/008', null, 'ASSE20260826_ALF';

-- modo nuevo: no debe tocar disco, devuelve 3 columnas
EXEC dbo.sp_XMLAsientosPru 'SINIE', '2026/008', null, 'ASSE20260826_ALF', 'PANTALLA';
