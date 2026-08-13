select AfectadoX, grupo, orden, SubGrupo
from Cardifwp.dbo.x100Grupo
where cast(AfectadoX as nvarchar(20)) in ('9001','9002','9004','8901','8902','8905');
