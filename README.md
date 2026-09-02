package co.com.bnpparibas.cardif.cierres.domain.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class XmlFileDto {
    private String journalType;
    private String fileName;
    private String content;
}


package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AccountingFileDto {
    private Integer id;
    private String product;
    private String journalType;
    private String fileName;
    private Date generationDate;
}


package co.com.bnpparibas.cardif.cierres.domain.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DownloadFileDto {
    private String fileName;
    private String content;
}
