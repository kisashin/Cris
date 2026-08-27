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
