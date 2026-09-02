            for (CSVRecord record : parser) {
                if (first) {
                    first = false;
                    if (isHeader(record)) {
                        continue;
                    }
                }

                if (record.size() < COLUMNS) {
                    incomplete++;
                }

                rows.add(toRow(record));
            }







    public List<String[]> read(MultipartFile file) {
        List<String[]> rows = new ArrayList<>();
        incomplete = 0;


    public int countIncomplete(List<String[]> rows) {
        return incomplete;
    }


    private int incomplete;    
