import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { HomologationPolicy } from '../models/HomologationPolicy.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class HomologationPolicyAlfaService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;

  constructor(private http: HttpClient) { }

  /**
   * Busca registros de homologación por código de producto.
   * Equivalente a CargarGridView1 del legacy.
   *
   * @param productCode Código de producto a buscar.
   * @returns Observable con la lista de registros encontrados.
   */
  buscarPorProducto(productCode: number): Observable<INewGeneralResponse<HomologationPolicy[]>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
    const params = new HttpParams().set('producto', productCode.toString());

    return this.http.get<INewGeneralResponse<HomologationPolicy[]>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa`,
      { headers, params }
    );
  }

  /**
   * Crea un nuevo registro de homologación.
   * Equivalente a BtnGuardar_Click con id = 0 del legacy.
   *
   * @param data Datos del nuevo registro.
   * @returns Observable con el registro creado.
   */
  crear(data: HomologationPolicy): Observable<INewGeneralResponse<HomologationPolicy>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.post<INewGeneralResponse<HomologationPolicy>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa`,
      data,
      { headers }
    );
  }

  /**
   * Edita un registro existente de homologación.
   * Equivalente a BtnGuardar_Click con id != 0 del legacy.
   *
   * @param id Identificador del registro a editar.
   * @param data Datos actualizados.
   * @returns Observable con el registro actualizado.
   */
  editar(id: number, data: HomologationPolicy): Observable<INewGeneralResponse<HomologationPolicy>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.put<INewGeneralResponse<HomologationPolicy>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa/${id}`,
      data,
      { headers }
    );
  }

  /**
   * Elimina un registro de homologación por su id.
   * Equivalente a btnEliminar_Click del legacy.
   *
   * @param id Identificador del registro a eliminar.
   * @returns Observable con la respuesta del servidor.
   */
  eliminar(id: number): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());

    return this.http.delete<INewGeneralResponse<string>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa/${id}`,
      { headers }
    );
  }
}
