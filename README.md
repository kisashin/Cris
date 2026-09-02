    @Test
    void loadClaims_devuelveElMensajeEnElCuerpo() {
        when(service.loadClaims(any(), anyString(), anyString()))
                .thenReturn(new LoadResultDto("5 Registros Cargados", 5, 1));

        BNPResponse response = controller.loadClaims(
                ClaimAccountingBuilder.csvFile("contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER);
        LoadResultDto body = (LoadResultDto) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals("5 Registros Cargados", body.getMessage());
        assertEquals(5, body.getTotalRows());
        assertEquals(1, body.getIncompleteRows());
    }

import static org.mockito.ArgumentMatchers.anyString;

import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadResultDto;    
