import java.util.function.Consumer;


    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(fullRow(), modified(row -> row.setCompania("99")));
        assertNotEquals(fullRow(), modified(row -> row.setSucursal("99")));
        assertNotEquals(fullRow(), modified(row -> row.setDescripcionRamo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setSymbol("X")));
        assertNotEquals(fullRow(), modified(row -> row.setRamo2(99)));
        assertNotEquals(fullRow(), modified(row -> row.setNroPoliza("X")));
        assertNotEquals(fullRow(), modified(row -> row.setModulo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCodBancoNegocio("X")));
        assertNotEquals(fullRow(), modified(row -> row.setDescripcionTomador("X")));
        assertNotEquals(fullRow(), modified(row -> row.setPolizaLiderAlfa("X")));
        assertNotEquals(fullRow(), modified(row -> row.setSiniestroLider("X")));
        assertNotEquals(fullRow(), modified(row -> row.setValor(99)));
        assertNotEquals(fullRow(), modified(row -> row.setNumeroLote(99)));
        assertNotEquals(fullRow(), modified(row -> row.setCampoUnion("X")));
        assertNotEquals(fullRow(), modified(row ->
                row.setValorInicialReserva(new BigDecimal("999.00"))));
        assertNotEquals(fullRow(), modified(row ->
                row.setValorAjustesReserva(new BigDecimal("999.00"))));
        assertNotEquals(fullRow(), modified(row ->
                row.setValorPagos(new BigDecimal("999.00"))));
        assertNotEquals(fullRow(), modified(row ->
                row.setValorActualReserva(new BigDecimal("999.00"))));
        assertNotEquals(fullRow(), modified(row -> row.setPorcentajeAlfa(99)));
        assertNotEquals(fullRow(), modified(row -> row.setValorGastosCoaseguro(99)));
        assertNotEquals(fullRow(), modified(row -> row.setValorSalvamento(99)));
        assertNotEquals(fullRow(), modified(row -> row.setValorRecuperaciones(99)));
        assertNotEquals(fullRow(), modified(row -> row.setNroidentificacion("X")));
        assertNotEquals(fullRow(), modified(row -> row.setNombreasegurado("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechanacimiento("X")));
        assertNotEquals(fullRow(), modified(row -> row.setEdad(99)));
        assertNotEquals(fullRow(), modified(row -> row.setSexo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setProfesion("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechaperdida("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechaaviso("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechareclamo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCodigoCausa("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCausaSiniestro("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCiudad("X")));
        assertNotEquals(fullRow(), modified(row -> row.setTipoSiniestro("X")));
        assertNotEquals(fullRow(), modified(row -> row.setNroCredito("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechadesembolso("X")));
        assertNotEquals(fullRow(), modified(row ->
                row.setPorcentajeAsegurabilidad("X")));
        assertNotEquals(fullRow(), modified(row -> row.setTipocredito("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCoberturaLider("X")));
        assertNotEquals(fullRow(), modified(row -> row.setReportadoPor("X")));
        assertNotEquals(fullRow(), modified(row -> row.setNitBeneficiario("X")));
        assertNotEquals(fullRow(), modified(row -> row.setBeneficiario("X")));
        assertNotEquals(fullRow(), modified(row -> row.setCausalObjecion("X")));
        assertNotEquals(fullRow(), modified(row -> row.setFechaObjecion("X")));
        assertNotEquals(fullRow(), modified(row -> row.setPlaca("X")));
        assertNotEquals(fullRow(), modified(row -> row.setSerial("X")));
        assertNotEquals(fullRow(), modified(row -> row.setMotor("X")));
        assertNotEquals(fullRow(), modified(row -> row.setTipoVehiculo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setClaseVehiculo("X")));
        assertNotEquals(fullRow(), modified(row -> row.setObservacionesPago("X")));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        AvalReportRow empty = new AvalReportRow();
        AvalReportRow other = new AvalReportRow();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setCompania("02");
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);

        assertNotNull(empty.toString());
    }

    private AvalReportRow modified(Consumer<AvalReportRow> change) {
        AvalReportRow row = fullRow();
        change.accept(row);
        return row;
    }
