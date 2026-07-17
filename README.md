AccountingEntryRowDto

package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.math.BigDecimal;

import lombok.Builder;
import lombok.Data;

/**
 * sp_AsientoSiniestrosAdicionales modo 1 (Generar): 27 columnas.
 * El orden DEBE coincidir con el SELECT del SP (mapeo posicional en el RepositoryImpl).
 */
@Data
@Builder
public class AccountingEntryRowDto {
	private String journalType;          // 1  cu.tipodiario
	private String accountingPeriod;     // 2  Periodo_contable
	private String transactionDate;      // 3  Fecha_transaccion
	private String accountCode;          // 4  cu.cuenta
	private String transactionReference; // 5  REF_TRANSACCION
	private String description;          // 6  SO.DESCRIPCION
	private String dueDate;              // 7  Fecha_Vencimiento
	private String currencyCode;         // 8  'COP'
	private BigDecimal transactionAmount;// 9  Importe_Transaccion
	private String baseAmount;           // 10 '0'
	private String debitCredit;          // 11 cu.naturaleza
	private String costCenter;           // 12 '99999'
	private String product;              // 13 co.producto
	private String branch;               // 14 co.ramo
	private String tax;                  // 15 '99'
	private String partner;              // 16 socio
	private String nit;                  // 17 so.nit
	private String advisorKey;           // 18 '9999999'
	private String coverage;             // 19 co.cobertura
	private String xDefine;              // 20 '0'
	private String planId;               // 21 '99999'
	private String journalSource;        // 22 'SSC'
	private String format;               // 23 '1;2'
	private String processDate;          // 24 Fecha_proceso
	private String entryDescription;     // 25 @ComentarioAsiento
	private String status;               // 26 'Pendiente XML'
	private String claimNumber;          // 27 Siniestro
}
