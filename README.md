    @SuppressWarnings("unchecked")
    private void mockReturningWork() {
        when(session.doReturningWork(any(ReturningWork.class)))
                .thenAnswer(invocation -> invocation
                        .getArgument(0, ReturningWork.class)
                        .execute(connection));
    }

        @Test
    @DisplayName("Should propagate errors raised by the mapper")
    void shouldPropagateMapperErrors() throws SQLException {
        ResultSet resultSet = mock(ResultSet.class);

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.next()).thenReturn(true);

        mockReturningWork();

        assertThrows(
                IllegalStateException.class,
                () -> executor.query(CALL, row -> {
                    throw new IllegalStateException("mapper error");
                }));
    }
