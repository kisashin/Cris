import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;


    List<AccountingFileDto> getFiles();

    DownloadFileDto downloadFile(Integer id);
