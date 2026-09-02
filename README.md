    XmlFileDto generateXml(String journalType, String period, String product, String comment);

    void deleteFiles(String product, String period);

    void saveFile(String product, String journalType, String period,
                  String fileName, String content, String user);

    List<AccountingFileDto> findFiles(String period);

    DownloadFileDto findFile(Integer id);


import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
