import { IAvalReportStatus } from '../models/aval-report-status.model';

  /**
   * Consulta el estado del reporte mensual de Aval.
   */
  findReportStatus(): Observable<INewGeneralResponse<IAvalReportStatus>> {
    return this.http.get<INewGeneralResponse<IAvalReportStatus>>(
      `${this.closingUrl}/report/status`,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Descarga el reporte mensual de Aval en formato Excel.
   */
  downloadAvalReport(): Observable<HttpResponse<Blob>> {
    return this.http.get(
      `${this.closingUrl}/report/download`,
      {
        headers: this.createHeaders(
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),
        observe: 'response',
        responseType: 'blob'
      }
    );
  }
