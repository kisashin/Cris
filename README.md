package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class AvalReportDtosTest {

    @Test
    @DisplayName("AvalReportRow builder asigna los valores")
    void reportRowBuilder() {
        AvalReportRow row = AvalReportRow.builder()
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

        assertEquals("02", row.getCompania());
        assertEquals("VIDA GRUPO", row.getDescripcionRamo());
        assertEquals(34, row.getRamo2());
        assertEquals("0902026A193877", row.getSiniestroLider());
        assertEquals(new BigDecimal("100.00"), row.getValorInicialReserva());
        assertEquals(new BigDecimal("400.00"), row.getValorActualReserva());
        assertEquals(100, row.getPorcentajeAlfa());
        assertEquals("JUAN PEREZ", row.getNombreasegurado());
        assertEquals(45, row.getEdad());
        assertEquals("HC", row.getCodigoCausa());
        assertEquals("Banco de Bogota", row.getBeneficiario());
        assertEquals("OBJ X MORA", row.getCausalObjecion());
        assertEquals("ABC123", row.getPlaca());
        assertEquals("SIN OBS", row.getObservacionesPago());
    }

    @Test
    @DisplayName("AvalReportRow setters y constructor vacio")
    void reportRowSetters() {
        AvalReportRow row = new AvalReportRow();

        assertNull(row.getCompania());

        row.setCompania("02");
        row.setSucursal("02");
        row.setSymbol("VG");
        row.setModulo("00");
        row.setValor(1);
        row.setNumeroLote(2);
        row.setValorPagos(new BigDecimal("500.00"));
        row.setEdad(30);
        row.setSexo("F");
        row.setCiudad("MEDELLIN");
        row.setSerial("SER999");
        row.setMotor("MOT999");
        row.setTipoVehiculo("MOTO");
        row.setClaseVehiculo("PARTICULAR");

        assertEquals("02", row.getCompania());
        assertEquals("02", row.getSucursal());
        assertEquals("VG", row.getSymbol());
        assertEquals("00", row.getModulo());
        assertEquals(1, row.getValor());
        assertEquals(2, row.getNumeroLote());
        assertEquals(new BigDecimal("500.00"), row.getValorPagos());
        assertEquals(30, row.getEdad());
        assertEquals("F", row.getSexo());
        assertEquals("MEDELLIN", row.getCiudad());
        assertEquals("SER999", row.getSerial());
        assertEquals("MOT999", row.getMotor());
        assertEquals("MOTO", row.getTipoVehiculo());
        assertEquals("PARTICULAR", row.getClaseVehiculo());
    }

    @Test
    @DisplayName("AvalReportStatusDTO builder, setters y constructores")
    void reportStatus() {
        AvalReportStatusDTO status = AvalReportStatusDTO.builder()
                .generationDate("27/08/2026 10:00:00 a. m.")
                .pendingMovements(93)
                .build();

        assertEquals("27/08/2026 10:00:00 a. m.",
                status.getGenerationDate());
        assertEquals(93, status.getPendingMovements());

        AvalReportStatusDTO empty = new AvalReportStatusDTO();
        empty.setGenerationDate("fecha");
        empty.setPendingMovements(0);

        assertEquals("fecha", empty.getGenerationDate());
        assertEquals(0, empty.getPendingMovements());

        AvalReportStatusDTO full =
                new AvalReportStatusDTO("otra fecha", 5);

        assertNotNull(full);
        assertEquals("otra fecha", full.getGenerationDate());
        assertEquals(5, full.getPendingMovements());
    }
}
