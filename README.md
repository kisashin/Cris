package co.com.bnpparibas.cardif.cierres.domain.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoadResultDto {
    private String message;
    private int totalRows;
    private int incompleteRows;
}


package co.com.bnpparibas.cardif.cierres.domain.util.helpers;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import co.com.bnpparibas.cardif.cierres.domain.util.constants.ExceptionConstants;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DataException;

@Component
public class ClaimFileHelper {

    public static final int COLUMNS = 46;

    private static final Charset ENCODING = Charset.forName("windows-1252");
    private static final char DELIMITER = ';';
    private static final String HEADER_FIRST_VALUE = "NORAMO";
    private static final String HEADER_SECOND_VALUE = "RAMO";

    private final List<String[]> rows = new ArrayList<>();

    public List<String[]> read(MultipartFile file) {
        rows.clear();

        CSVFormat format = CSVFormat.DEFAULT
                .withDelimiter(DELIMITER)
                .withIgnoreEmptyLines(true)
                .withTrim(false);

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(file.getInputStream(), ENCODING));
             CSVParser parser = new CSVParser(reader, format)) {

            boolean first = true;

            for (CSVRecord record : parser) {
                if (first) {
                    first = false;
                    if (isHeader(record)) {
                        continue;
                    }
                }
                rows.add(toRow(record));
            }
        } catch (IOException e) {
            throw new DataException(ExceptionConstants.FILE_READ_ERROR, e);
        }

        if (rows.isEmpty()) {
            throw new DataException(ExceptionConstants.FILE_WITHOUT_RECORDS);
        }

        return new ArrayList<>(rows);
    }

    public int countIncomplete(List<String[]> records) {
        int incomplete = 0;

        for (String[] row : records) {
            if (row[COLUMNS - 1] == null) {
                incomplete++;
            }
        }

        return incomplete;
    }

    private boolean isHeader(CSVRecord record) {
        if (record.size() == 0) {
            return false;
        }

        String value = record.get(0) == null ? "" : record.get(0).trim().toUpperCase();

        return HEADER_FIRST_VALUE.equals(value) || HEADER_SECOND_VALUE.equals(value);
    }

    private String[] toRow(CSVRecord record) {
        String[] row = new String[COLUMNS];

        for (int i = 0; i < COLUMNS && i < record.size(); i++) {
            String value = record.get(i);
            row[i] = value == null || value.isEmpty() ? null : value;
        }

        return row;
    }
}
