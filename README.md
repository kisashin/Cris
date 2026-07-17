ClaimAccountingBuilder

package co.com.bnpparibas.cardif.builders;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;

public class ClaimAccountingBuilder {

	private ClaimAccountingBuilder() { }

	public static final String PRODUCT = "2005";
	public static final String COMMENT = "2005_202406";

	public static LoadClaimRequestDto loadRequest() {
		LoadClaimRequestDto r = new LoadClaimRequestDto();
		r.setProduct(PRODUCT);
		return r;
	}

	public static GenerateAccountingRequestDto generateRequest() {
		GenerateAccountingRequestDto r = new GenerateAccountingRequestDto();
		r.setProduct(PRODUCT);
		r.setComment(COMMENT);
		return r;
	}

	public static SendAccountingRequestDto sendRequest() {
		SendAccountingRequestDto r = new SendAccountingRequestDto();
		r.setProduct(PRODUCT);
		r.setComment(COMMENT);
		r.setUserName("AM\\bermudezma");
		return r;
	}

	/** Fila cruda del modo 1 (27 columnas) en el orden EXACTO del SELECT del SP. */
	public static Object[] entryRowMode1() {
		return new Object[] {
			"SINIE", "2024/006", "20240630", "51144000", "Avisos", "SOCIO X S.A.",
			"30/06/2024", "COP", "150000", "0", "D", "99999", "0430", "31", "99",
			"20", "830000000", "9999999", "99999", "0", "99999", "SSC", "1;2",
			"20240630", COMMENT, "Pendiente XML", "SIN-001"
		};
	}

	/** Fila cruda del modo 3 (6 columnas). */
	public static Object[] totalRowMode3() {
		return new Object[] { "0430", "SINIE", "Avisos", "51144000", "150000", "0" };
	}
}
