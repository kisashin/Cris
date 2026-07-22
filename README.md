POST http://localhost:9091/ws_cierres/v1/claim-accounting/total-by-account
{ "product": "2012", "comment": "2012_202602" }


List<Object[]> rows = callProcedure(SP_ASIENTO, 3, comment, product);
log.info("totalByAccount filas: {}", rows.size());
return rows.stream()
        .map(row -> AccountTotalRowDto.builder()
        ...
