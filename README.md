ClaimAccountingRepository

package co.com.bnpparibas.cardif.cierres.infraestructure.repository;

import java.util.List;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;

public interface ClaimAccountingRepository {

	/** fFecha2Txt(...,'') => YYYYMMDD (para el front). */
	String getAccountingDate();

	/** fFecha2Txt(...,'/') => YYYY/MM/DD (base del periodo canónico YYYY/0MM). */
	String getAccountingPeriodRaw();

	List<String> getProducts();

	int countProductLayout(String product);

	/** true => sp_CargaSiniestrosAlfa (layout=1); false => sp_CargaSiniestros. */
	String loadClaims(String product, boolean alpha);

	List<AccountingEntryRowDto> generateEntry(String comment, String product);

	List<AccountTotalRowDto> totalByAccount(String comment, String product);

	void registerEntry(String comment, String product);

	void markXmlGenerated(String comment, String product);

	String generateXml(String journalType, String period, String product, String comment);

	void notifyByMail(String xmlName, String userName, String body);
}
