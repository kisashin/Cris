package co.com.bnpparibas.cardif.builders;

import java.nio.charset.Charset;
import java.sql.Timestamp;

import org.springframework.mock.web.MockMultipartFile;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;

public class ClaimAccountingBuilder {

    private ClaimAccountingBuilder() {
    }

    public static final String PRODUCT = "2012";
    public static final String COMMENT = "2012_202602";
    public static final String PERIOD_RAW = "2026/02/01";
    public static final String PERIOD = "2026/002";
    public static final String USER = "j36147";
    public static final String XML_CONTENT = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC/>";
    public static final String FILE_NAME = "2012_202602SINIE_2012202602.XML";

    public static final String PATTERN = "326CO21SR012";
    public static final String CSV_NAME = "326CO21SR0122026090110.csv";
    public static final Charset CSV_CHARSET = Charset.forName("windows-1252");

    private static final int COLUMNS = 46;

    public static GenerateAccountingRequestDto generateRequest() {
        GenerateAccountingRequestDto request = new GenerateAccountingRequestDto();
        request.setProduct(PRODUCT);
        request.setComment(COMMENT);
        return request;
    }

    public static RegisterAccountingRequestDto registerRequest() {
        RegisterAccountingRequestDto request = new RegisterAccountingRequestDto();
        request.setProduct(PRODUCT);
        request.setComment(COMMENT);
        return request;
    }

    public static SendAccountingRequestDto sendRequest() {
        SendAccountingRequestDto request = new SendAccountingRequestDto();
        request.setProduct(PRODUCT);
        request.setComment(COMMENT);
        request.setUser(USER);
        return request;
    }

    public static Object[] entryRow() {
        return new Object[] {
                "SINIE", "2026/002", "20260201", "51144000", "Pago Definitivo", "SOCIO",
                "01/02/2026", "COP", "150000", "0", "D", "99999", "2012", "34", "99",
                "20", "830000000", "9999999", "99999", "0", "99999", "SSC", "1;2",
                "20260201", COMMENT, "Pendiente XML", "SIN-001"
        };
    }

    public static Object[] totalRow() {
        return new Object[] { "2012", "SINIE", "Pago Definitivo", "51144000", "150000", "0" };
    }

    public static XmlFileDto xmlFile(String journalType) {
        return new XmlFileDto(journalType, journalType + "_" + PRODUCT + ".XML", XML_CONTENT);
    }

    public static Object[] xmlRow() {
        return new Object[] { "SINIE", FILE_NAME, XML_CONTENT };
    }

    public static Object[] fileRow() {
        return new Object[] { 1, PRODUCT, "SINIE", FILE_NAME,
                Timestamp.valueOf("2026-09-02 03:04:45") };
    }

    public static String csvHeader() {
        return "NoRAMO;RAMO;SINIESTRO;T_PAGO;SUC;SIMB;POLIZA;VIG;ASEGURADO;CC_ASEGURADO;"
                + "TOMADOR;RES_ANTERIOR;AVISOS;PAGO_DEFINITIVO;SOBREPAGO;LIBERACIONES_rebajas;"
                + "INCREMENTOS;CANCELACIONES_liberaciones;REVERSIONES;RES_ACTUAL;RECUP_PAGOS;"
                + "FECHA_PAGO;LIDER;FECHA_STRO;FECHA_AVISO;FECHA_RECLAMO;REPORTADO;VLR_RECLAMO;"
                + "DESCRIPCION;CAUSA;LUGAR;OBSERVACIONES;CREDITO;VLR_DESEMBOLSO;FECHA_DESEMB;"
                + "PORCASEGU;GENERO;EDAD;LINEA_DE_CREDITO;USUARIO_RES;USUARIO_ANALIS;"
                + "USUARIO_PAGO;COD_AJUSTADOR;FECHA_OBJECION;PERFIL;ESTADO";
    }

    /** Fila con el numero de campos indicado; el primero lleva el valor recibido. */
    public static String csvRow(String first, int fields) {
        StringBuilder row = new StringBuilder(first);

        for (int i = 1; i < fields; i++) {
            row.append(';').append("V").append(i);
        }

        return row.toString();
    }

    public static String csvRow(String first) {
        return csvRow(first, COLUMNS);
    }

    public static MockMultipartFile csvFile(String name, String content) {
        return new MockMultipartFile("file", name, "text/csv", content.getBytes(CSV_CHARSET));
    }

    public static MockMultipartFile csvFile(String content) {
        return csvFile(CSV_NAME, content);
    }
}
