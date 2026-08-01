import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';

import { PartnerReportService } from '../../services/partner-report.service';
import { ReportStatus } from '../../models/report-status.model';
import { FlagCode } from '../../../../shared/constants/flag-codes';

@Component({
  selector: 'app-partner-report-ca',
  templateUrl: './partner-report-ca.component.html',
  styleUrls: ['./partner-report-ca.component.scss'],
  standalone: false
})
export class PartnerReportCAComponent implements OnInit {

  private readonly uploadFlag = FlagCode.CA;

  displayedColumns: any[] = [
    { title: 'ESTADO', field: 'status' },
    { title: 'FECHA PROCESO', field: 'dateProcessing' },
    { title: 'REPORTE DATOS', field: 'reportData' },
    { title: 'REPORTE MOVIMIENTOS', field: 'reportMovements' }
  ];

  listFields = this.displayedColumns.map(el => el.field);

  dataSource: ReportStatus[] = [];

  loading = false;

  constructor(
    private readonly partnerReportService: PartnerReportService,
    private readonly toastr: ToastrService
  ) {
  }

  ngOnInit(): void {
    this.loadData();
  }

  /**
   * Loads Central America reports.
   */
  loadData(): void {

    this.loading = true;

    this.partnerReportService
      .getAllReports(this.uploadFlag)
      .pipe(
        finalize(() => this.loading = false)
      )
      .subscribe({

        next: response => {

          this.dataSource = response;

        },

        error: () => {

          this.toastr.error(
            'Error cargando reportes.'
          );

        }

      });

  }

  /**
   * Sends report generation request.
   */
  sendReport(): void {

    this.loading = true;

    this.partnerReportService
      .updateReports(
        null,
        null,
        this.uploadFlag
      )
      .pipe(
        finalize(() => this.loading = false)
      )
      .subscribe({

        next: () => {

          this.toastr.success(
            'Aceptado!! En Proceso.'
          );

          this.loadData();

        },

        error: () => {

          this.toastr.error(
            'Error generando el reporte.'
          );

        }

      });

  }

}


import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { map } from 'rxjs/operators';  
import { ReportStatus } from '../models/report-status.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PartnerReportService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;

  constructor (private http: HttpClient){}

  getAllReports(countryCode?: String): Observable<ReportStatus[]> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', countryCode?.trim() || crypto.randomUUID())

    return this.http
      .get<INewGeneralResponse<ReportStatus[]>>(
        `${this.baseUrl}/v1/all-partner-reports`,
        { headers }
      )
      .pipe(
        map(resp => resp.bodyResponse ?? [])
      );
  }

  updateReports(dateFrom: string | null, dateUntil: string | null, countryCode?: String): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', countryCode?.trim() || crypto.randomUUID())
      .set('Content-Type', 'application/json')
      .set('Accept', 'text/plain');

    const body = { dateFrom: dateFrom ?? null, dateUntil: dateUntil ?? null };

    return this.http.post<string>(
      `${this.baseUrl}/v1/update-partner-report`,
      body,
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

}
