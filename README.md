src/app/views/claims-closing/services/cardif-peru-closing.service.ts
src/app/views/claims-closing/services/cardif-peru-closing.service.spec.ts

import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { INewGeneralResponse } from '../models/new-general-response.interface';

/**
 * Servicio del cierre de movimientos Cardif Perú.
 *
 * <p>Consume los endpoints del backend ws-closing-claims:
 * PUT /v1/cardif-peru-closing/generate (ejecuta la contabilización) y
 * GET /v1/cardif-peru-closing/download (descarga el reporte en Excel).</p>
 *
 * <p>Los headers correlation_id, request_id y _p se generan aquí porque el
 * interceptor de la aplicación no los inyecta (solo agrega UID_USER y el
 * spinner).</p>
 */
@Injectable({
  providedIn: 'root'
})
export class CardifPeruClosingService {

  private readonly baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/cardif-peru-closing`;

  private readonly correlationId = crypto.randomUUID();

  constructor(private readonly http: HttpClient) {}

  /**
   * Ejecuta la generación de los asientos contables (procedimiento).
   */
  generateAccountingEntries(): Observable<INewGeneralResponse<string>> {
    return this.http.put<INewGeneralResponse<string>>(
      `${this.baseUrl}/generate`,
      null,
      {
        headers: this.createHeaders('application/json')
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
