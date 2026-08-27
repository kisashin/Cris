export interface IColombiaXmlFile {
  id: number;
  period: string;
  family: string;
  movementType: string;
  fileName: string;
  lineCount: number;
  processDate: string;
  status: string;
}

export interface IColombiaAccountingResult {
  message: string;
  period: string;
  files: IColombiaXmlFile[];
}



import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { catchError, map } from 'rxjs/operators'; 
import { ReportStatus } from '../models/report-status.model';
import { environment } from 'src/environments/environment';
import {
  IColombiaAccountingResult,
  IColombiaXmlFile
} from '../models/colombia-accounting-result.model';

@Injectable({
  providedIn: 'root',
})
export class ClosingCardifService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;
  private readonly closingUrl = `${this.baseUrl}/v1/cardif-closing`;
  private readonly correlationId = crypto.randomUUID();

  constructor (private http: HttpClient){}

  getAllReportsDetailsCardif(): Observable<ReportStatus[]> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http
      .get<INewGeneralResponse<ReportStatus[]>>(
        `${this.baseUrl}/v1/all-cardif-reports`,
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

  updateReportsCardif(): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.put<string>(
      `${this.baseUrl}/v1/update-cardif-report`,
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
