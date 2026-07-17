import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../../environments/environment';
import { AccountingRequest } from '../models/accounting-request.model';
import { LoadClaimsRequest } from '../models/accounting-request.model';

@Injectable({
  providedIn: 'root'
})
export class AccountingEntryService {

  // OJO: el back expone /v1/claim-accounting. Antes faltaba el /v1 => 404 en todo.
  private readonly url = `${environment.urlAPICierresBackEnd}/v1/claim-accounting`;

  constructor(
    private http: HttpClient
  ) { }

  getAccountingDate(): Observable<any> {
    return this.http.get<any>(`${this.url}/accounting-date`);
  }

  getProducts(): Observable<any> {
    return this.http.get<any>(`${this.url}/products`);
  }

  loadClaims(request: LoadClaimsRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/load`, request);
  }

  // antes /preview  ->  el back es /generate
  previewAccountingEntry(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/generate`, request);
  }

  registerAccountingEntry(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/register`, request);
  }

  // antes /account-summary  ->  el back es /total-by-account
  getAccountSummary(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/total-by-account`, request);
  }

  sendAccountingEntry(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/send`, request);
  }

  // downloadExcel ELIMINADO: el botón XLS del legacy no funciona y no se migra.
}
