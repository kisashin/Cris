package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SendResponseDto {
	private List<String> files;
	private String message;
}
