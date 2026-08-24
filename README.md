import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import {
  IAccountingXmlFile,
  ICenterAccountingResult
} from '../models/center-accounting-result.model';

/**
 * Servicio del cierre contable Centroamerica.
 */
@Injectable({
  providedIn: 'root'
})
export class AccountingClosingCaService {

  private readonly baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/cardif-center-closing`;

  private readonly correlationId = crypto.randomUUID();

  constructor(private readonly http: HttpClient) {}

  /**
   * Ejecuta la generacion de los asientos contables.
   */
  generateAccountingEntries(): Observable<INewGeneralResponse<ICenterAccountingResult>> {
    return this.http.put<INewGeneralResponse<ICenterAccountingResult>>(
      `${this.baseUrl}/generate`,
      null,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Consulta los archivos XML generados en procesos anteriores.
   */
  findGeneratedFiles(): Observable<INewGeneralResponse<IAccountingXmlFile[]>> {
    return this.http.get<INewGeneralResponse<IAccountingXmlFile[]>>(
      `${this.baseUrl}/files`,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Descarga el contenido de un archivo XML persistido.
   */
  downloadXmlFile(id: number): Observable<HttpResponse<Blob>> {
    return this.http.get(
      `${this.baseUrl}/files/${id}/download`,
      {
        headers: this.createHeaders('application/xml'),
        observe: 'response',
        responseType: 'blob'
      }
    );
  }

  /**
   * Descarga el reporte de movimientos en formato Excel.
   */
  downloadMovementsReport(): Observable<HttpResponse<Blob>> {
    return this.http.get(
      `${this.baseUrl}/download`,
      {
        headers: this.createHeaders(
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),
        observe: 'response',
        responseType: 'blob'
      }
    );
  }

  private createHeaders(accept: string): HttpHeaders {
    return new HttpHeaders()
      .set('correlation_id', this.correlationId)
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID())
      .set('Accept', accept);
  }
}
