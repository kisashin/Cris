import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { catchError, map } from 'rxjs/operators'; 
import { ClosingStatus } from '../models/closing-aval.model';
import { environment } from 'src/environments/environment';
import {
  IColombiaAccountingResult,
  IColombiaXmlFile
} from '../models/colombia-accounting-result.model';

@Injectable({
  providedIn: 'root',
})
export class ClosingAvalService {
  
  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;
  private readonly closingUrl = `${this.baseUrl}/v1/aval-closing`;
  private readonly correlationId = crypto.randomUUID();

  constructor (private http: HttpClient){}

  getAllReportsDetailsAval(): Observable<ClosingStatus[]> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http
      .get<INewGeneralResponse<ClosingStatus[]>>(
        `${this.baseUrl}/v1/all-aval-details-reports`,
        { headers }
      )
      .pipe(
        map(resp => resp.bodyResponse ?? []),
        catchError(err => {
          const msg = err?.error?.errorDetail?.message ?? err?.error?.message ?? '';
          if (err.status === 400 && msg.includes('No registros')) {
            return of([]);
          }
          throw err;
        })
      );
  }

  updateReportsAval(): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.put<string>(
      `${this.baseUrl}/v1/update-aval-report`,
      null,
      { 
        headers,
        responseType: 'text' as 'json'
      }
    ).pipe(
      map((txt: string) => ({
        bodyResponse: txt
      }) as INewGeneralResponse<string>)
    );
  }

  getAllReportsSeatAval(): Observable<ClosingStatus[]> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http
      .get<INewGeneralResponse<ClosingStatus[]>>(
        `${this.baseUrl}/v1/all-seat-aval-details-reports`,
        { headers }
      )
      .pipe(
        map(resp => resp.bodyResponse ?? [])
      );
  }

  updateReportsSeatAval(): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.put<string>(
      `${this.baseUrl}/v1/update-seat-aval-report`,
      null,
      { 
        headers,
        responseType: 'text' as 'json'
      }
    ).pipe(
      map((txt: string) => ({
        bodyResponse: txt
      }) as INewGeneralResponse<string>)
    );
  }

  /**
   * Ejecuta la generacion de los asientos contables.
   */
  generateAccountingEntries(): Observable<INewGeneralResponse<IColombiaAccountingResult>> {
    return this.http.put<INewGeneralResponse<IColombiaAccountingResult>>(
      `${this.closingUrl}/generate`,
      null,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Consulta los archivos XML generados en procesos anteriores.
   */
  findGeneratedFiles(): Observable<INewGeneralResponse<IColombiaXmlFile[]>> {
    return this.http.get<INewGeneralResponse<IColombiaXmlFile[]>>(
      `${this.closingUrl}/files`,
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
      `${this.closingUrl}/files/${id}/download`,
      {
        headers: this.createHeaders('application/xml'),
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
