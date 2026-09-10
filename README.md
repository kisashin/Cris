import { IAvalReportFile } from '../models/aval-report-status.model';


  /**
   * Consulta el estado del reporte mensual de Aval.
   */
  findReportStatus(): Observable<INewGeneralResponse<IAvalReportFile>> {
    return this.http.get<INewGeneralResponse<IAvalReportFile>>(
      `${this.closingUrl}/report/status`,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Genera y persiste el reporte mensual de Aval.
   */
  generateAvalReport(): Observable<INewGeneralResponse<IAvalReportFile>> {
    return this.http.put<INewGeneralResponse<IAvalReportFile>>(
      `${this.closingUrl}/report/generate`,
      null,
      {
        headers: this.createHeaders('application/json')
      }
    );
  }

  /**
   * Descarga el reporte mensual de Aval persistido.
   */
  downloadAvalReport(id: number): Observable<HttpResponse<Blob>> {
    return this.http.get(
      `${this.closingUrl}/report/${id}/download`,
      {
        headers: this.createHeaders(
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),
        observe: 'response',
        responseType: 'blob'
      }
    );
  }
