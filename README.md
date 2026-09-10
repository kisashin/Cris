import { IAvalReportFile } from '../models/aval-report-status.model';


  describe('#findReportStatus', () => {
    it('should GET the report status', () => {
      const status: IAvalReportFile = {
        id: 1,
        period: '202609',
        fileName: 'RPT_CIERRE_AVAL.xlsx',
        rowCount: 257,
        processDate: '09/09/2026 10:00:00 a. m.',
        status: 'GENERADO',
        pendingMovements: 93
      };

      service.findReportStatus().subscribe(response => {
        expect(response.bodyResponse?.pendingMovements).toBe(93);
        expect(response.bodyResponse?.fileName)
          .toBe('RPT_CIERRE_AVAL.xlsx');
      });

      const request = httpMock.expectOne(`${closingUrl}/report/status`);
      expect(request.request.method).toBe('GET');
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush({ bodyResponse: status });
    });
  });

  describe('#generateAvalReport', () => {
    it('should PUT the report generation request', () => {
      service.generateAvalReport().subscribe(response => {
        expect(response.bodyResponse?.id).toBe(1);
      });

      const request = httpMock.expectOne(`${closingUrl}/report/generate`);
      expect(request.request.method).toBe('PUT');
      expect(request.request.body).toBeNull();
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush({
        bodyResponse: {
          id: 1,
          fileName: 'RPT_CIERRE_AVAL.xlsx',
          rowCount: 257,
          pendingMovements: 93
        }
      });
    });
  });

  describe('#downloadAvalReport', () => {
    it('should GET the Excel report as Blob', () => {
      const mockBlob = new Blob(['excel'], {
        type:
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      });

      const responseHeaders = new HttpHeaders({
        'Content-Disposition': 'attachment; filename="RPT_CIERRE_AVAL.xlsx"'
      });

      service.downloadAvalReport(1).subscribe(response => {
        expect(response.body).toEqual(mockBlob);
        expect(response.headers.get('Content-Disposition'))
          .toContain('RPT_CIERRE_AVAL.xlsx');
      });

      const request = httpMock.expectOne(`${closingUrl}/report/1/download`);
      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expect(request.request.headers.get('Accept')).toBe(
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      );

      request.flush(mockBlob, {
        headers: responseHeaders,
        status: 200,
        statusText: 'OK'
      });
    });
  });

  
