package co.com.bnpparibas.cardif.builders;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;

public class ClaimAccountingBuilder {

	private ClaimAccountingBuilder() {
	}

	public static final String PRODUCT = "2012";
	public static final String COMMENT = "2012_202602";
	public static final String PERIOD_RAW = "2026/02/01";
	public static final String PERIOD = "2026/002";

	public static LoadClaimRequestDto loadRequest() {
		LoadClaimRequestDto request = new LoadClaimRequestDto();
		request.setProduct(PRODUCT);
		return request;
	}

	public static GenerateAccountingRequestDto generateRequest() {
		GenerateAccountingRequestDto request = new GenerateAccountingRequestDto();
		request.setProduct(PRODUCT);
		request.setComment(COMMENT);
		return request;
	}

	public static RegisterAccountingRequestDto registerRequest() {
		RegisterAccountingRequestDto request = new RegisterAccountingRequestDto();
		request.setProduct(PRODUCT);
		request.setComment(COMMENT);
		return request;
	}

	public static SendAccountingRequestDto sendRequest() {
		SendAccountingRequestDto request = new SendAccountingRequestDto();
		request.setProduct(PRODUCT);
		request.setComment(COMMENT);
		return request;
	}

	public static Object[] entryRow() {
		return new Object[] {
			"SINIE", "2026/002", "20260201", "51144000", "Pago Definitivo", "SOCIO",
			"01/02/2026", "COP", "150000", "0", "D", "99999", "2012", "34", "99",
			"20", "830000000", "9999999", "99999", "0", "99999", "SSC", "1;2",
			"20260201", COMMENT, "Pendiente XML", "SIN-001"
		};
	}

	public static Object[] totalRow() {
		return new Object[] { "2012", "SINIE", "Pago Definitivo", "51144000", "150000", "0" };
	}
}
