HomologationPolicyAlfaControllerTest — buildRequest() y buildResponse():
javaprivate HomologationPolicyResponseDTO buildResponse() {
    return HomologationPolicyResponseDTO.builder()
            .id(1)
            .productCode(749)
            .branchCode(31)
            .policyNumber("0000490")
            .appliesValidity(0)
            .startDate(LocalDate.of(2024, 1, 1))
            .endDate(LocalDate.of(2024, 12, 31))
            .build();
}

private HomologationPolicyRequestDTO buildRequest() {
    HomologationPolicyRequestDTO req = new HomologationPolicyRequestDTO();
    req.setProductCode(749);
    req.setBranchCode(31);
    req.setPolicyNumber("0000490");
    req.setAppliesValidity(0);
    req.setStartDate(LocalDate.of(2024, 1, 1));
    req.setEndDate(LocalDate.of(2024, 12, 31));
    return req;
}
Y en el test crear_shouldReturn201WithCreatedRecord cambiar:
java// Mal
assertEquals(749, response.getBody().getBodyResponse().getProducto());
// Bien
assertEquals(749, response.getBody().getBodyResponse().getProductCode());

HomologationPolicyAlfaServiceImplTest — buildEntity() y buildRequest():
javaprivate HomologationPolicyAlfa buildEntity() {
    HomologationPolicyAlfa e = new HomologationPolicyAlfa();
    e.setId(1);
    e.setProducto(749);    // entity mantiene español — va a BD
    e.setRamo(31);
    e.setNroPoliza("0000490");
    e.setAplicaVigencia(0);
    e.setFechaInicio(LocalDate.of(2024, 1, 1));
    e.setFechaFin(LocalDate.of(2024, 12, 31));
    return e;
}

private HomologationPolicyRequestDTO buildRequest() {
    HomologationPolicyRequestDTO req = new HomologationPolicyRequestDTO();
    req.setProductCode(749);
    req.setBranchCode(31);
    req.setPolicyNumber("0000490");
    req.setAppliesValidity(0);
    req.setStartDate(LocalDate.of(2024, 1, 1));
    req.setEndDate(LocalDate.of(2024, 12, 31));
    return req;
}
Y en los asserts dentro de los tests:
java// Mal
assertEquals(749, result.get(0).getProducto());
assertEquals("0000490", result.get(0).getNroPoliza());
assertEquals(749, result.getProducto());

// Bien
assertEquals(749, result.get(0).getProductCode());
assertEquals("0000490", result.get(0).getPolicyNumber());
assertEquals(749, result.getProductCode());
