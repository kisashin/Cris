
    import java.sql.ResultSetMetaData;
    
    public <T> List<T> query(
            String call,
            StoredProcedureRowMapper<T> mapper,
            String requiredColumn) {

        return entityManager.unwrap(Session.class)
                .doReturningWork(connection -> {
                    List<T> rows = new ArrayList<>();

                    try (CallableStatement statement =
                                 connection.prepareCall(call)) {

                        statement.setQueryTimeout(timeoutSeconds);
                        boolean hasResultSet = statement.execute();

                        while (hasResultSet
                                || statement.getUpdateCount() != -1) {

                            if (hasResultSet) {
                                readMatchingResultSet(
                                        statement,
                                        mapper,
                                        rows,
                                        requiredColumn);
                            }

                            hasResultSet = statement.getMoreResults();
                        }
                    }

                    return rows;
                });
    }

    private <T> void readMatchingResultSet(
            CallableStatement statement,
            StoredProcedureRowMapper<T> mapper,
            List<T> rows,
            String requiredColumn) throws SQLException {

        try (ResultSet resultSet = statement.getResultSet()) {

            if (!hasColumn(resultSet, requiredColumn)) {
                return;
            }

            while (resultSet.next()) {
                rows.add(mapper.map(resultSet));
            }
        }
    }

    private boolean hasColumn(
            ResultSet resultSet,
            String columnName) throws SQLException {

        ResultSetMetaData metaData = resultSet.getMetaData();

        for (int index = 1; index <= metaData.getColumnCount(); index++) {
            if (columnName.equalsIgnoreCase(metaData.getColumnLabel(index))) {
                return true;
            }
        }

        return false;
    }
