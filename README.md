package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AvalReportRowTest {

    private AvalReportRow fullRow() {
        return AvalReportRow.builder()
                .compania("02")
                .sucursal("02")
                .descripcionRamo("VIDA GRUPO")
                .symbol("VG")
                .ramo2(34)
                .nroPoliza("123")
                .modulo("00")
                .codBancoNegocio("4020")
                .descripcionTomador("Banco de Bogota")
                .polizaLiderAlfa("456")
                .siniestroLider("0902026A193877")
                .valor(0)
                .numeroLote(0)
                .campoUnion("0902026A193877")
                .valorInicialReserva(new BigDecimal("100.00"))
                .valorAjustesReserva(new BigDecimal("200.00"))
                .valorPagos(new BigDecimal("300.00"))
                .valorActualReserva(new BigDecimal("400.00"))
                .porcentajeAlfa(100)
                .valorGastosCoaseguro(0)
                .valorSalvamento(0)
                .valorRecuperaciones(0)
                .nroidentificacion("1020304050")
                .nombreasegurado("JUAN PEREZ")
                .fechanacimiento("19800101")
                .edad(45)
                .sexo("M")
                .profesion("INGENIERO")
                .fechaperdida("20260801")
                .fechaaviso("20260805")
                .fechareclamo("20260805")
                .codigoCausa("HC")
                .causaSiniestro("MUERTE ACCIDENTAL")
                .ciudad("BOGOTA")
                .tipoSiniestro("OT")
                .nroCredito("998877")
                .fechadesembolso("20250101")
                .porcentajeAsegurabilidad("100")
                .tipocredito("LIBRE INVERSION")
                .coberturaLider("MUERTE ACCIDENTAL")
                .reportadoPor("Pago")
                .nitBeneficiario("8600029644")
                .beneficiario("Banco de Bogota")
                .causalObjecion("OBJ X MORA")
                .fechaObjecion("20260810")
                .placa("ABC123")
                .serial("SER123")
                .motor("MOT123")
                .tipoVehiculo("AUTO")
                .claseVehiculo("PARTICULAR")
                .observacionesPago("SIN OBS")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AvalReportRow row = fullRow();

        assertEquals("02", row.getCompania());
        assertEquals("02", row.getSucursal());
        assertEquals("VIDA GRUPO", row.getDescripcionRamo());
        assertEquals("VG", row.getSymbol());
        assertEquals(34, row.getRamo2());
        assertEquals("123", row.getNroPoliza());
        assertEquals("00", row.getModulo());
        assertEquals("4020", row.getCodBancoNegocio());
        assertEquals("Banco de Bogota", row.getDescripcionTomador());
        assertEquals("456", row.getPolizaLiderAlfa());
        assertEquals("0902026A193877", row.getSiniestroLider());
        assertEquals(0, row.getValor());
        assertEquals(0, row.getNumeroLote());
        assertEquals("0902026A193877", row.getCampoUnion());
        assertEquals(new BigDecimal("100.00"), row.getValorInicialReserva());
        assertEquals(new BigDecimal("200.00"), row.getValorAjustesReserva());
        assertEquals(new BigDecimal("300.00"), row.getValorPagos());
        assertEquals(new BigDecimal("400.00"), row.getValorActualReserva());
        assertEquals(100, row.getPorcentajeAlfa());
        assertEquals(0, row.getValorGastosCoaseguro());
        assertEquals(0, row.getValorSalvamento());
        assertEquals(0, row.getValorRecuperaciones());
        assertEquals("1020304050", row.getNroidentificacion());
        assertEquals("JUAN PEREZ", row.getNombreasegurado());
        assertEquals("19800101", row.getFechanacimiento());
        assertEquals(45, row.getEdad());
        assertEquals("M", row.getSexo());
        assertEquals("INGENIERO", row.getProfesion());
        assertEquals("20260801", row.getFechaperdida());
        assertEquals("20260805", row.getFechaaviso());
        assertEquals("20260805", row.getFechareclamo());
        assertEquals("HC", row.getCodigoCausa());
        assertEquals("MUERTE ACCIDENTAL", row.getCausaSiniestro());
        assertEquals("BOGOTA", row.getCiudad());
        assertEquals("OT", row.getTipoSiniestro());
        assertEquals("998877", row.getNroCredito());
        assertEquals("20250101", row.getFechadesembolso());
        assertEquals("100", row.getPorcentajeAsegurabilidad());
        assertEquals("LIBRE INVERSION", row.getTipocredito());
        assertEquals("MUERTE ACCIDENTAL", row.getCoberturaLider());
        assertEquals("Pago", row.getReportadoPor());
        assertEquals("8600029644", row.getNitBeneficiario());
        assertEquals("Banco de Bogota", row.getBeneficiario());
        assertEquals("OBJ X MORA", row.getCausalObjecion());
        assertEquals("20260810", row.getFechaObjecion());
        assertEquals("ABC123", row.getPlaca());
        assertEquals("SER123", row.getSerial());
        assertEquals("MOT123", row.getMotor());
        assertEquals("AUTO", row.getTipoVehiculo());
        assertEquals("PARTICULAR", row.getClaseVehiculo());
        assertEquals("SIN OBS", row.getObservacionesPago());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AvalReportRow row = new AvalReportRow();

        assertNull(row.getCompania());

        row.setCompania("02");
        row.setSucursal("02");
        row.setDescripcionRamo("VIDA GRUPO");
        row.setSymbol("VG");
        row.setRamo2(34);
        row.setNroPoliza("123");
        row.setModulo("00");
        row.setCodBancoNegocio("4020");
        row.setDescripcionTomador("Banco de Bogota");
        row.setPolizaLiderAlfa("456");
        row.setSiniestroLider("0902026A193877");
        row.setValor(1);
        row.setNumeroLote(2);
        row.setCampoUnion("0902026A193877");
        row.setValorInicialReserva(new BigDecimal("100.00"));
        row.setValorAjustesReserva(new BigDecimal("200.00"));
        row.setValorPagos(new BigDecimal("500.00"));
        row.setValorActualReserva(new BigDecimal("400.00"));
        row.setPorcentajeAlfa(100);
        row.setValorGastosCoaseguro(0);
        row.setValorSalvamento(0);
        row.setValorRecuperaciones(0);
        row.setNroidentificacion("1020304050");
        row.setNombreasegurado("JUAN PEREZ");
        row.setFechanacimiento("19800101");
        row.setEdad(30);
        row.setSexo("F");
        row.setProfesion("INGENIERO");
        row.setFechaperdida("20260801");
        row.setFechaaviso("20260805");
        row.setFechareclamo("20260805");
        row.setCodigoCausa("HC");
        row.setCausaSiniestro("MUERTE ACCIDENTAL");
        row.setCiudad("MEDELLIN");
        row.setTipoSiniestro("OT");
        row.setNroCredito("998877");
        row.setFechadesembolso("20250101");
        row.setPorcentajeAsegurabilidad("100");
        row.setTipocredito("LIBRE INVERSION");
        row.setCoberturaLider("MUERTE ACCIDENTAL");
        row.setReportadoPor("Pago");
        row.setNitBeneficiario("8600029644");
        row.setBeneficiario("Banco de Bogota");
        row.setCausalObjecion("OBJ X MORA");
        row.setFechaObjecion("20260810");
        row.setPlaca("ABC123");
        row.setSerial("SER999");
        row.setMotor("MOT999");
        row.setTipoVehiculo("MOTO");
        row.setClaseVehiculo("PARTICULAR");
        row.setObservacionesPago("SIN OBS");

        assertEquals("02", row.getCompania());
        assertEquals("02", row.getSucursal());
        assertEquals("VIDA GRUPO", row.getDescripcionRamo());
        assertEquals("VG", row.getSymbol());
        assertEquals(34, row.getRamo2());
        assertEquals("123", row.getNroPoliza());
        assertEquals("00", row.getModulo());
        assertEquals("4020", row.getCodBancoNegocio());
        assertEquals("Banco de Bogota", row.getDescripcionTomador());
        assertEquals("456", row.getPolizaLiderAlfa());
        assertEquals("0902026A193877", row.getSiniestroLider());
        assertEquals(1, row.getValor());
        assertEquals(2, row.getNumeroLote());
        assertEquals("0902026A193877", row.getCampoUnion());
        assertEquals(new BigDecimal("100.00"), row.getValorInicialReserva());
        assertEquals(new BigDecimal("200.00"), row.getValorAjustesReserva());
        assertEquals(new BigDecimal("500.00"), row.getValorPagos());
        assertEquals(new BigDecimal("400.00"), row.getValorActualReserva());
        assertEquals(100, row.getPorcentajeAlfa());
        assertEquals(0, row.getValorGastosCoaseguro());
        assertEquals(0, row.getValorSalvamento());
        assertEquals(0, row.getValorRecuperaciones());
        assertEquals("1020304050", row.getNroidentificacion());
        assertEquals("JUAN PEREZ", row.getNombreasegurado());
        assertEquals("19800101", row.getFechanacimiento());
        assertEquals(30, row.getEdad());
        assertEquals("F", row.getSexo());
        assertEquals("INGENIERO", row.getProfesion());
        assertEquals("20260801", row.getFechaperdida());
        assertEquals("20260805", row.getFechaaviso());
        assertEquals("20260805", row.getFechareclamo());
        assertEquals("HC", row.getCodigoCausa());
        assertEquals("MUERTE ACCIDENTAL", row.getCausaSiniestro());
        assertEquals("MEDELLIN", row.getCiudad());
        assertEquals("OT", row.getTipoSiniestro());
        assertEquals("998877", row.getNroCredito());
        assertEquals("20250101", row.getFechadesembolso());
        assertEquals("100", row.getPorcentajeAsegurabilidad());
        assertEquals("LIBRE INVERSION", row.getTipocredito());
        assertEquals("MUERTE ACCIDENTAL", row.getCoberturaLider());
        assertEquals("Pago", row.getReportadoPor());
        assertEquals("8600029644", row.getNitBeneficiario());
        assertEquals("Banco de Bogota", row.getBeneficiario());
        assertEquals("OBJ X MORA", row.getCausalObjecion());
        assertEquals("20260810", row.getFechaObjecion());
        assertEquals("ABC123", row.getPlaca());
        assertEquals("SER999", row.getSerial());
        assertEquals("MOT999", row.getMotor());
        assertEquals("MOTO", row.getTipoVehiculo());
        assertEquals("PARTICULAR", row.getClaseVehiculo());
        assertEquals("SIN OBS", row.getObservacionesPago());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AvalReportRow row = new AvalReportRow(
                "02", "02", "VIDA GRUPO", "VG", 34, "123", "00", "4020",
                "Banco de Bogota", "456", "0902026A193877", 0, 0,
                "0902026A193877", new BigDecimal("100.00"),
                new BigDecimal("200.00"), new BigDecimal("300.00"),
                new BigDecimal("400.00"), 100, 0, 0, 0, "1020304050",
                "JUAN PEREZ", "19800101", 45, "M", "INGENIERO", "20260801",
                "20260805", "20260805", "HC", "MUERTE ACCIDENTAL", "BOGOTA",
                "OT", "998877", "20250101", "100", "LIBRE INVERSION",
                "MUERTE ACCIDENTAL", "Pago", "8600029644", "Banco de Bogota",
                "OBJ X MORA", "20260810", "ABC123", "SER123", "MOT123",
                "AUTO", "PARTICULAR", "SIN OBS");

        assertNotNull(row);
        assertEquals("02", row.getCompania());
        assertEquals("SIN OBS", row.getObservacionesPago());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AvalReportRow first = fullRow();
        AvalReportRow second = fullRow();
        AvalReportRow different = fullRow();
        different.setCompania("99");

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AvalReportRow());
        assertTrue(first.toString().contains("JUAN PEREZ"));
    }
}
