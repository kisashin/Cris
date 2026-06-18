src/app/views/claims-closing/services/peru-accounting-report.service.spec.ts

import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpHeaders } from '@angular/common/http';

import { environment } from 'src/environments/environment';
import { PeruAccountingReportService } from './peru-accounting-report.service';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { PeruAccountingReportResponse } from '../models/peru-accounting-report.model';

describe('PeruAccountingReportService', () => {
  let service: PeruAccountingReportService;
  let httpMock: HttpTestingController;

  const baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/peru-accounting-report`;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [PeruAccountingReportService]
    });

    service = TestBed.inject(PeruAccountingReportService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getLatestReportDate', () => {
    it('should GET the latest report date', () => {
      const mockResponse:
        INewGeneralResponse<PeruAccountingReportResponse> = {
          correlationId: 'correlation-id',
          responseHeader: {
            returnCode: 200,
            message: 'Success'
          },
          bodyResponse: {
            reportDate: '2026-06-16T10:30:00'
          }
        };

      service.getLatestReportDate().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const request = httpMock.expectOne(`${baseUrl}/latest`);

      expect(request.request.method).toBe('GET');
      expect(request.request.headers.has('correlation_id')).toBeTrue();
      expect(request.request.headers.has('request_id')).toBeTrue();
      expect(request.request.headers.has('_p')).toBeTrue();
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush(mockResponse);
    });
  });

  describe('#generateReport', () => {
    it('should PUT the report generation request', () => {
      const mockResponse: INewGeneralResponse<string> = {
        correlationId: 'correlation-id',
        responseHeader: {
          returnCode: 200,
          message: 'Success'
        },
        bodyResponse:
          'Información del reporte contable generada correctamente.'
      };

      service.generateReport().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const request = httpMock.expectOne(`${baseUrl}/generate`);

      expect(request.request.method).toBe('PUT');
      expect(request.request.body).toBeNull();
      expect(request.request.headers.has('correlation_id')).toBeTrue();
      expect(request.request.headers.has('request_id')).toBeTrue();
      expect(request.request.headers.has('_p')).toBeTrue();
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush(mockResponse);
    });
  });

  describe('#downloadReport', () => {
    it('should GET the Excel report as Blob', () => {
      const mockBlob = new Blob(
        ['excel-content'],
        {
          type:
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
      );

      const responseHeaders = new HttpHeaders({
        'Content-Disposition':
          'attachment; filename="ReporteContablePeru.xlsx"'
      });

      service.downloadReport().subscribe(response => {
        expect(response.body).toEqual(mockBlob);
        expect(
          response.headers.get('Content-Disposition')
        ).toContain('ReporteContablePeru.xlsx');
      });

      const request = httpMock.expectOne(`${baseUrl}/download`);

      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expect(request.request.headers.has('correlation_id')).toBeTrue();
      expect(request.request.headers.has('request_id')).toBeTrue();
      expect(request.request.headers.has('_p')).toBeTrue();
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
});

ng test --include="**/peru-accounting-report.service.spec.ts"
