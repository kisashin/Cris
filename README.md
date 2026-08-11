import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import {
  ClaimMovement,
  IndividualNews,
  IndividualNewsDeleteRequest,
  IndividualNewsRequest
} from '../models/IndividualNews.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class IndividualNewsService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;

  constructor(private http: HttpClient) { }

  private buildHeaders(): HttpHeaders {
    return new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
  }

  /**
   * Consulta los movimientos de un siniestro sin novedad pendiente.
   *
   * @param claimNumber Número de siniestro a consultar.
   * @returns Observable con los movimientos disponibles.
   */
  buscarMovimientos(claimNumber: string): Observable<INewGeneralResponse<ClaimMovement[]>> {
    const params = new HttpParams().set('numeroSiniestro', claimNumber);

    return this.http.get<INewGeneralResponse<ClaimMovement[]>>(
      `${this.baseUrl}/v1/novedades-individuales/movimientos`,
      { headers: this.buildHeaders(), params }
    );
  }

  /**
   * Consulta un movimiento por su identificador Carvajal.
   *
   * @param idCarvajal Identificador del movimiento.
   * @returns Observable con el movimiento consultado.
   */
  consultarMovimiento(idCarvajal: number): Observable<INewGeneralResponse<ClaimMovement>> {
    return this.http.get<INewGeneralResponse<ClaimMovement>>(
      `${this.baseUrl}/v1/novedades-individuales/movimientos/${idCarvajal}`,
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Registra una solicitud de actualización sobre un movimiento.
   *
   * @param data Nuevos valores del movimiento.
   * @returns Observable con la novedad creada.
   */
  solicitarActualizacion(data: IndividualNewsRequest): Observable<INewGeneralResponse<IndividualNews>> {
    return this.http.post<INewGeneralResponse<IndividualNews>>(
      `${this.baseUrl}/v1/novedades-individuales/actualizaciones`,
      data,
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Registra una solicitud de eliminación sobre un movimiento.
   *
   * @param data Identificador y justificación.
   * @returns Observable con la novedad creada.
   */
  solicitarEliminacion(data: IndividualNewsDeleteRequest): Observable<INewGeneralResponse<IndividualNews>> {
    return this.http.post<INewGeneralResponse<IndividualNews>>(
      `${this.baseUrl}/v1/novedades-individuales/eliminaciones`,
      data,
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Consulta las novedades pendientes de autorización.
   *
   * @returns Observable con las novedades pendientes.
   */
  consultarPendientes(): Observable<INewGeneralResponse<IndividualNews[]>> {
    return this.http.get<INewGeneralResponse<IndividualNews[]>>(
      `${this.baseUrl}/v1/novedades-individuales`,
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Consulta el detalle de una novedad pendiente.
   *
   * @param code Identificador de la novedad.
   * @returns Observable con la novedad consultada.
   */
  consultarNovedad(code: number): Observable<INewGeneralResponse<IndividualNews>> {
    return this.http.get<INewGeneralResponse<IndividualNews>>(
      `${this.baseUrl}/v1/novedades-individuales/${code}`,
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Aplica una novedad pendiente sobre el histórico de movimientos.
   *
   * @param code Identificador de la novedad.
   * @returns Observable con la novedad procesada.
   */
  aprobar(code: number): Observable<INewGeneralResponse<IndividualNews>> {
    return this.http.post<INewGeneralResponse<IndividualNews>>(
      `${this.baseUrl}/v1/novedades-individuales/${code}/aprobar`,
      {},
      { headers: this.buildHeaders() }
    );
  }

  /**
   * Cancela una novedad pendiente.
   *
   * @param code Identificador de la novedad.
   * @returns Observable con la novedad cancelada.
   */
  cancelar(code: number): Observable<INewGeneralResponse<IndividualNews>> {
    return this.http.post<INewGeneralResponse<IndividualNews>>(
      `${this.baseUrl}/v1/novedades-individuales/${code}/cancelar`,
      {},
      { headers: this.buildHeaders() }
    );
  }
}