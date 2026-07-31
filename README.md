import { Injectable } from '@angular/core';
import { ReportStatusPageDTO } from '../models/report-status.model';
import { Observable } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ReportStatusClaimServiceService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;

  constructor(private http: HttpClient) { }

  getReportStatus(page?: number, pageSize?: number, partner?: String): Observable<INewGeneralResponse<ReportStatusPageDTO>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', partner?.trim() || crypto.randomUUID());
    let params = new HttpParams();
    if (page !== undefined) {
      params = params.set('page', page.toString());
    }
    if (pageSize !== undefined) {
      params = params.set('pageSize', pageSize.toString());
    }
    return this.http.get<INewGeneralResponse<ReportStatusPageDTO>>(`${this.baseUrl}/v1/report-status-claim`, { headers, params }
    );
  }

  changeStatusFileData(partner?: String): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', partner?.trim() || crypto.randomUUID());
    return this.http.put<INewGeneralResponse<string>>(`${this.baseUrl}/v1/change-file-data`, null, { headers }
    );
  }
}
