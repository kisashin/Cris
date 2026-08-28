import java.sql.ResultSet;
import java.sql.SQLException;

import org.mockito.ArgumentCaptor;

import static org.mockito.Mockito.mock;



    @Nested
    @DisplayName("Mapeo de resultados")
    class RowMapping {

        @SuppressWarnings("unchecked")
        private StoredProcedureRowMapper<ColombiaAccountingLine>
                captureAccountingMapper() {

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(xmlHelper.buildFiles(anyList()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            ArgumentCaptor<StoredProcedureRowMapper<ColombiaAccountingLine>>
                    captor = ArgumentCaptor.forClass(
                            StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor).query(
                    anyString(), captor.capture(), anyString());

            return captor.getValue();
        }

        @Test
        @DisplayName("debe mapear la linea contable desde el ResultSet")
        void shouldMapAccountingLine() throws SQLException {
            StoredProcedureRowMapper<ColombiaAccountingLine> mapper =
                    captureAccountingMapper();

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString("Familia")).thenReturn("ReasegAlfa");
            when(resultSet.getString("Periodo")).thenReturn("202608");
            when(resultSet.getInt("Pasada")).thenReturn(1);
            when(resultSet.getString("Mv")).thenReturn("Constitucion");
            when(resultSet.getString("NombreArchivo")).thenReturn(null);
            when(resultSet.getLong("Secuencia")).thenReturn(7L);
            when(resultSet.getString("Line")).thenReturn("<Line/>");

            ColombiaAccountingLine line = mapper.map(resultSet);

            assertEquals("ReasegAlfa", line.getFamily());
            assertEquals("202608", line.getPeriod());
            assertEquals(1, line.getPass());
            assertEquals("Constitucion", line.getMovementType());
            assertNull(line.getFileName());
            assertEquals(7L, line.getSequence());
            assertEquals("<Line/>", line.getContent());
        }

        @SuppressWarnings("unchecked")
        @Test
        @DisplayName("debe mapear la fila del reporte desde el ResultSet")
        void shouldMapReportRow() throws Exception {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            ArgumentCaptor<StoredProcedureRowMapper<AvalReportRow>>
                    captor = ArgumentCaptor.forClass(
                            StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(), captor.capture(), anyString());

            StoredProcedureRowMapper<AvalReportRow> mapper =
                    captor.getAllValues().get(1);

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString(anyString())).thenReturn("valor");
            when(resultSet.getInt(anyString())).thenReturn(5);
            when(resultSet.getBigDecimal(anyString()))
                    .thenReturn(new java.math.BigDecimal("10.00"));
            when(resultSet.wasNull()).thenReturn(false);

            AvalReportRow row = mapper.map(resultSet);

            assertNotNull(row);
            assertEquals("valor", row.getCompania());
            assertEquals(5, row.getRamo2());
            assertEquals(
                    new java.math.BigDecimal("10.00"),
                    row.getValorPagos());
            assertEquals("valor", row.getObservacionesPago());
        }

        @SuppressWarnings("unchecked")
        @Test
        @DisplayName("debe devolver null cuando el entero viene nulo")
        void shouldReturnNullWhenIntegerIsNull() throws Exception {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            ArgumentCaptor<StoredProcedureRowMapper<AvalReportRow>>
                    captor = ArgumentCaptor.forClass(
                            StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(), captor.capture(), anyString());

            StoredProcedureRowMapper<AvalReportRow> mapper =
                    captor.getAllValues().get(1);

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString(anyString())).thenReturn(null);
            when(resultSet.getInt(anyString())).thenReturn(0);
            when(resultSet.getBigDecimal(anyString())).thenReturn(null);
            when(resultSet.wasNull()).thenReturn(true);

            AvalReportRow row = mapper.map(resultSet);

            assertNotNull(row);
            assertNull(row.getRamo2());
            assertNull(row.getEdad());
            assertNull(row.getValorPagos());
        }

        @SuppressWarnings("unchecked")
        @Test
        @DisplayName("debe descartar el resultado del procedimiento de reporte")
        void shouldDiscardReportProcedureResult() throws Exception {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            ArgumentCaptor<StoredProcedureRowMapper<Object>>
                    captor = ArgumentCaptor.forClass(
                            StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(), captor.capture(), anyString());

            StoredProcedureRowMapper<Object> mapper =
                    captor.getAllValues().get(0);

            assertNull(mapper.map(mock(ResultSet.class)));
        }
    }
