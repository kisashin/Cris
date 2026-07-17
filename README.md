AccountTotalRowDto

package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.math.BigDecimal;

import lombok.Builder;
import lombok.Data;

/** sp_AsientoSiniestrosAdicionales modo 3 (Total x Cuenta): 6 columnas. */
@Data
@Builder
public class AccountTotalRowDto {
	private String product;              // Producto
	private String journalType;          // Tipo_diario
	private String transactionReference; // Ref_transaccion
	private String accountCode;          // Codigo_cuenta
	private BigDecimal debit;            // Debito
	private BigDecimal credit;           // Credito
}
