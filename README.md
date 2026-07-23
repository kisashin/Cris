package co.com.bnpparibas.cardif.cierres.domain.service;

import java.util.List;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingDateResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;

public interface ClaimAccountingService {

	AccountingDateResponseDto getAccountingDate();

	List<ProductResponseDto> getProducts();

	LoadMessageResponseDto loadClaims(LoadClaimRequestDto request);

	List<AccountingEntryRowDto> generateEntry(GenerateAccountingRequestDto request);

	List<AccountTotalRowDto> totalByAccount(GenerateAccountingRequestDto request);

	void registerEntry(RegisterAccountingRequestDto request);

	SendResponseDto sendEntry(SendAccountingRequestDto request);
}
