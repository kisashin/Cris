package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.KeyClaimPageDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.InconsistentCoverageResponseDto;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportFileResponseDto;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportStatusResponseDto;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportStatusPageDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportTabularDto;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.FileData;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.FileDataExt;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.FileDataExtRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.FileDataRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ReportDataRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ReportStoredProcedureRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ReportDataServiceImplTest {

    @InjectMocks
    private ReportDataServiceImpl reportDataService;

    @Mock
    private FileDataRepository fileDataRepository;

    @Mock
    private FileDataExtRepository fileDataExtRepository;

    @Mock
    private ReportDataRepository reportDataRepository;

    @Mock
    private ReportStoredProcedureRepository reportStoredProcedureRepository;

    private static final String P_HEADER = "pHeaderValue";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID = "req-456";

    private static final String SP_DATA = "dbo.SP_Reporte_Datos_Siniestros";
    private static final String SP_MOVEMENTS = "dbo.SP_Reporte_Movimientos_Siniestros";

    /** Construye un resultado tabular de prueba con cabeceras y filas. */
    private ReportTabularDto buildTabular() {

        List<String> headers = Arrays.asList("Llavesiniestro", "Socio", "Edad");

        List<String[]> rows = new ArrayList<>();
        rows.add(new String[]{"089102L64996162-DESEMPLEO", "BANISTMO S.A", "43"});
        rows.add(new String[]{"089102M06622162-DESEMPLEO", "BANISTMO S.A", "53"});

        return new ReportTabularDto(headers, rows);
    }

    // =========================
    // EXISTENTES
    // =========================

    @Test
    void getReportData() {

        FileData fileData = new FileData();
        fileData.setId(1L);

        Page<FileData> page = mock(Page.class);

        when(page.getContent()).thenReturn(Collections.singletonList(fileData));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(3);
        when(page.getTotalElements()).thenReturn(1L);

        when(fileDataRepository.findAll((Pageable) any())).thenReturn(page);

        ReportStatusPageDTO result =
                reportDataService.getReportData("p", "ci", "rq", 1, 10);

        assertNotNull(result);
    }

    @Test
    void changeStatusFileData() {

        when(fileDataRepository.changeStatusFile()).thenReturn(1);

        String rs = reportDataService.changeStatusFileData(
                P_HEADER, CORRELATION_ID, REQUEST_ID);

        assertNotNull(rs);
    }

    @Test
    void changeStatusFileDataError() {

        when(fileDataRepository.changeStatusFile())
                .thenThrow(new RuntimeException());

        BusinessException ex = assertThrows(BusinessException.class,
                () -> reportDataService.changeStatusFileData(
                        P_HEADER, CORRELATION_ID, REQUEST_ID));

        assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
    }

    @Test
    void getKeyClaims() {

        Page<FileDataRepository.LlaveSiniestroProjection> page = mock(Page.class);

        when(page.getContent()).thenReturn(Collections.emptyList());
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(3);
        when(page.getTotalElements()).thenReturn(1L);

        when(fileDataRepository.findKeyClaims(any(Pageable.class)))
                .thenReturn(page);

        KeyClaimPageDTO rs =
                reportDataService.getKeyClaims(P_HEADER, CORRELATION_ID, REQUEST_ID, 0, 10);

        assertNotNull(rs);
    }

    @Test
    void getReportDataPeru() {

        FileDataExt fileDataExt = new FileDataExt();
        fileDataExt.setId(1L);

        Page<FileDataExt> page = mock(Page.class);

        when(page.getContent()).thenReturn(Collections.singletonList(fileDataExt));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(2);
        when(page.getTotalElements()).thenReturn(1L);

        when(fileDataExtRepository.findAll(any(Pageable.class)))
                .thenReturn(page);

        ReportStatusPageDTO response =
                reportDataService.getReportData("51", CORRELATION_ID, REQUEST_ID, 0, 10);

        assertNotNull(response);
    }

    @Test
    void getReportDataWithNullPagination() {

        Page<FileData> page = mock(Page.class);

        when(page.getContent()).thenReturn(Collections.emptyList());
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(0);
        when(page.getTotalElements()).thenReturn(0L);

        when(fileDataRepository.findAll(any(Pageable.class)))
                .thenReturn(page);

        ReportStatusPageDTO response =
                reportDataService.getReportData(P_HEADER, CORRELATION_ID, REQUEST_ID, null, null);

        assertNotNull(response);
        verify(fileDataRepository).findAll(any(Pageable.class));
    }

    @Test
    void changeStatusFileDataPeru() {

        when(fileDataExtRepository.changeStatusFile())
                .thenReturn(1);

        String response =
                reportDataService.changeStatusFileData("51", CORRELATION_ID, REQUEST_ID);

        assertEquals("Aceptado!! En Proceso.", response);

        verify(fileDataExtRepository).changeStatusFile();
        verify(fileDataRepository, never()).changeStatusFile();
    }

    @Test
    void changeStatusFileDataPeruError() {

        when(fileDataExtRepository.changeStatusFile())
                .thenThrow(new RuntimeException("error"));

        BusinessException exception = assertThrows(BusinessException.class,
                () -> reportDataService.changeStatusFileData(
                        "51", CORRELATION_ID, REQUEST_ID));

        assertEquals(HttpStatus.PRECONDITION_FAILED, exception.getHttpStatus());
    }

    @Test
    void getKeyClaimsPeru() {

        FileDataExtRepository.LlaveSiniestroExtProjection projection =
                mock(FileDataExtRepository.LlaveSiniestroExtProjection.class);

        when(projection.getLlavesiniestros()).thenReturn("SIN123");

        Page<FileDataExtRepository.LlaveSiniestroExtProjection> page =
                mock(Page.class);

        when(page.getContent()).thenReturn(Collections.singletonList(projection));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(1);
        when(page.getTotalElements()).thenReturn(1L);

        when(fileDataExtRepository.findKeyClaims(any(Pageable.class)))
                .thenReturn(page);

        KeyClaimPageDTO response =
                reportDataService.getKeyClaims("51", CORRELATION_ID, REQUEST_ID, 0, 10);

        assertNotNull(response);
        assertEquals(1, response.getKeyClaimDTOS().size());
    }

    @Test
    void getKeyClaimsShouldFilterInvalidKeys() {

        FileDataRepository.LlaveSiniestroProjection valid =
                mock(FileDataRepository.LlaveSiniestroProjection.class);

        FileDataRepository.LlaveSiniestroProjection invalid =
                mock(FileDataRepository.LlaveSiniestroProjection.class);

        when(valid.getLlavesiniestros()).thenReturn("SIN123");
        when(invalid.getLlavesiniestros()).thenReturn(".");

        Page<FileDataRepository.LlaveSiniestroProjection> page =
                mock(Page.class);

        when(page.getContent()).thenReturn(Arrays.asList(valid, invalid));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(1);
        when(page.getTotalElements()).thenReturn(2L);

        when(fileDataRepository.findKeyClaims(any(Pageable.class)))
                .thenReturn(page);

        KeyClaimPageDTO response =
                reportDataService.getKeyClaims(P_HEADER, CORRELATION_ID, REQUEST_ID, 0, 10);

        assertEquals(1, response.getKeyClaimDTOS().size());
    }

    @Test
    void getKeyClaimsShouldFilterNullValues() {

        FileDataRepository.LlaveSiniestroProjection valid =
                mock(FileDataRepository.LlaveSiniestroProjection.class);

        when(valid.getLlavesiniestros()).thenReturn("SIN123");

        Page<FileDataRepository.LlaveSiniestroProjection> page =
                mock(Page.class);

        when(page.getContent()).thenReturn(Arrays.asList(valid, null));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(1);
        when(page.getTotalElements()).thenReturn(2L);

        when(fileDataRepository.findKeyClaims(any(Pageable.class)))
                .thenReturn(page);

        KeyClaimPageDTO response =
                reportDataService.getKeyClaims(P_HEADER, CORRELATION_ID, REQUEST_ID, 0, 10);

        assertEquals(1, response.getKeyClaimDTOS().size());
    }

    // =========================
    // REPORT STATUS
    // =========================

    @Test
    void getReportStatus_empty() {

        when(reportDataRepository.findAllReportStatus())
                .thenReturn(Collections.emptyList());

        List<ReportStatusResponseDto> result =
                reportDataService.getReportStatus();

        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    void getReportStatus_null() {

        when(reportDataRepository.findAllReportStatus())
                .thenReturn(null);

        List<ReportStatusResponseDto> result =
                reportDataService.getReportStatus();

        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    void getReportStatus_success() {

        ReportDataRepository.ReportStatusProjection projection =
                mock(ReportDataRepository.ReportStatusProjection.class);

        when(projection.getId()).thenReturn(1);
        when(projection.getFechaproceso()).thenReturn(LocalDateTime.now());
        when(projection.getEstado()).thenReturn("OK");

        when(reportDataRepository.findAllReportStatus())
                .thenReturn(Collections.singletonList(projection));

        List<ReportStatusResponseDto> result =
                reportDataService.getReportStatus();

        assertEquals(1, result.size());
        assertEquals(Integer.valueOf(1), result.get(0).getId());
    }

    // =========================
    // GENERATE REPORT
    // =========================

    @Test
    void generateReport_shouldDelegateToRepository() {

        reportDataService.generateReport();

        verify(reportDataRepository).generateReport();
    }

    // =========================
    // GET REPORT
    // =========================

    @Test
    void getReport_nullType_shouldThrowBusinessException() {

        BusinessException ex = assertThrows(BusinessException.class,
                () -> reportDataService.getReport(null));

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());

        verify(reportStoredProcedureRepository, never()).execute(anyString());
    }

    @Test
    void getReport_invalidType_shouldThrowBusinessException() {

        BusinessException ex = assertThrows(BusinessException.class,
                () -> reportDataService.getReport("INVALID"));

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());

        verify(reportStoredProcedureRepository, never()).execute(anyString());
    }

    @Test
    void getReport_data_success() {

        when(reportStoredProcedureRepository.execute(SP_DATA))
                .thenReturn(buildTabular());

        ReportFileResponseDto result =
                reportDataService.getReport("datos");

        assertNotNull(result);
        assertEquals("RptDatos.xlsx", result.getFileName());
        assertEquals(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                result.getFileType());
        assertNotNull(result.getFileBase64());
        assertFalse(result.getFileBase64().isEmpty());

        verify(reportStoredProcedureRepository).execute(SP_DATA);
    }

    @Test
    void getReport_movements_success() {

        when(reportStoredProcedureRepository.execute(SP_MOVEMENTS))
                .thenReturn(buildTabular());

        ReportFileResponseDto result =
                reportDataService.getReport("movimientos");

        assertNotNull(result);
        assertEquals("RptMovimientos.xlsx", result.getFileName());
        assertNotNull(result.getFileBase64());

        verify(reportStoredProcedureRepository).execute(SP_MOVEMENTS);
    }

    @Test
    void getReport_typeIsCaseInsensitive() {

        when(reportStoredProcedureRepository.execute(SP_DATA))
                .thenReturn(buildTabular());

        ReportFileResponseDto result =
                reportDataService.getReport("DATOS");

        assertEquals("RptDatos.xlsx", result.getFileName());
    }

    /** Sin filas pero con cabeceras: se genera el archivo solo con encabezados. */
    @Test
    void getReport_withHeadersAndNoRows_shouldGenerateFile() {

        ReportTabularDto onlyHeaders = new ReportTabularDto(
                Arrays.asList("Llavesiniestro", "Socio"),
                Collections.emptyList());

        when(reportStoredProcedureRepository.execute(SP_DATA))
                .thenReturn(onlyHeaders);

        ReportFileResponseDto result =
                reportDataService.getReport("datos");

        assertNotNull(result.getFileBase64());
        assertFalse(result.getFileBase64().isEmpty());
    }

    /** Sin metadata: el procedimiento no devolvio result set. */
    @Test
    void getReport_withoutColumns_shouldThrowBusinessException() {

        when(reportStoredProcedureRepository.execute(SP_DATA))
                .thenReturn(ReportTabularDto.empty());

        BusinessException ex = assertThrows(BusinessException.class,
                () -> reportDataService.getReport("datos"));

        assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
    }

    // =========================
    // INCONSISTENT COVERAGES
    // =========================

    @Test
    void getInconsistentCoverages_success() {

        ReportDataRepository.InconsistentCoverageProjection projection =
                mock(ReportDataRepository.InconsistentCoverageProjection.class);

        when(projection.getLlavesiniestros()).thenReturn("SIN-123");

        when(reportDataRepository.findInconsistentCoverages())
                .thenReturn(Collections.singletonList(projection));

        List<InconsistentCoverageResponseDto> result =
                reportDataService.getInconsistentCoverages();

        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("SIN-123", result.get(0).getLlavesiniestros());
    }

    @Test
    void getInconsistentCoverages_empty() {

        when(reportDataRepository.findInconsistentCoverages())
                .thenReturn(Collections.emptyList());

        List<InconsistentCoverageResponseDto> result =
                reportDataService.getInconsistentCoverages();

        assertNotNull(result);
        assertTrue(result.isEmpty());
    }
}
