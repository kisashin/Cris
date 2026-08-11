package co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IndividualNewsResponseDTO {

    private Long code;
    private Long idCarvajal;
    private String claimNumber;
    private String newsType;
    private String status;
    private String justification;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime processDate;

    private String requestUser;
    private String authorizerUser;
}