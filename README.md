src/app/views/claims-closing/models/peru-accounting-report.model.ts

export interface PeruAccountingReportResponse {
  reportDate: string | null;
}


src/app/views/claims-closing/services/peru-accounting-report.service.ts


import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { PeruAccountingReportResponse } from '../models/peru-accounting-report.model';

@Injectable({
  providedIn: 'root'
})
export class PeruAccountingReportService {

  private readonly baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/peru-accounting-report`;

  private readonly correlationId = crypto.randomUUID();

  constructor(private readonly http: HttpClient) {}

  /**
   * Consulta la fecha de la última generación del reporte.
   */
  getLatestReportDate():
    Observable<INewGeneralResponse<PeruAccountingReportResponse>> {

    return this.http.get<
      INewGeneralResponse<PeruAccountingReportResponse>
    >(
      `${this.baseUrl}/latest`,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Ejecuta la generación de la información del reporte contable.
   */
  generateReport(): Observable<INewGeneralResponse<string>> {
    return this.http.put<INewGeneralResponse<string>>(
      `${this.baseUrl}/generate`,
      null,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Descarga el reporte contable en formato Excel.
   */
  downloadReport(): Observable<HttpResponse<Blob>> {
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
