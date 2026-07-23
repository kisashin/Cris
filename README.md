package co.com.bnpparibas.cardif.cierres.infraestructure.repository;

import java.util.List;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;

public interface ClaimAccountingRepository {

	String getAccountingDate();

	String getAccountingPeriodRaw();

	List<String> getProducts();

	int countProductLayout(String product);

	String loadClaims(String product, boolean alpha);

	List<AccountingEntryRowDto> generateEntry(String comment, String product);

	List<AccountTotalRowDto> totalByAccount(String comment, String product);

	void registerEntry(String comment, String product);

	void markXmlGenerated(String comment, String product);

	String generateXml(String journalType, String period, String product, String comment);
}
