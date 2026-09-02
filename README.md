        assertEquals("02/09/2026 03:04:45", files.get(0).getGenerationDate());


    @Test
    void findFiles_conFechaNulaDevuelveCampoNulo() {
        mockNativeQuery(null, Collections.singletonList(
                new Object[] { 1, ClaimAccountingBuilder.PRODUCT, "SINIE",
                        ClaimAccountingBuilder.FILE_NAME, null }));

        assertNull(repository.findFiles(ClaimAccountingBuilder.PERIOD).get(0).getGenerationDate());
    }        
