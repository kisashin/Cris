import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../../../environments/environment';
import {
  AccountingRequest,
  SendAccountingRequest
} from '../models/accounting-request.model';

@Injectable({
  providedIn: 'root'
})
export class AccountingEntryService {

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

  loadClaims(file: File, product: string, user: string): Observable<any> {

    const formData = new FormData();

    formData.append('file', file, file.name);
    formData.append('product', product);
    formData.append('user', user);

    return this.http.post<any>(`${this.url}/load`, formData);
  }

  previewAccountingEntry(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/generate`, request);
  }

  registerAccountingEntry(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/register`, request);
  }

  getAccountSummary(request: AccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/total-by-account`, request);
  }

  sendAccountingEntry(request: SendAccountingRequest): Observable<any> {
    return this.http.post<any>(`${this.url}/send`, request);
  }

  getFiles(): Observable<any> {
    return this.http.get<any>(`${this.url}/files`);
  }

  downloadFile(id: number): Observable<HttpResponse<Blob>> {
    return this.http.get(
      `${this.url}/files/${id}/download`,
      {
        observe: 'response',
        responseType: 'blob'
      }
    );
  }
}
