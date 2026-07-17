AccountingEntryResponseDto

package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.math.BigDecimal;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AccountingEntryResponseDto {

    private String account;
    private String description;
    private BigDecimal debit;
    private BigDecimal credit;
}
