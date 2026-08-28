import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ClosingAvalService } from './closing-aval.service';
import { IColombiaXmlFile } from '../models/colombia-accounting-result.model';
import { IAvalReportStatus } from '../models/aval-report-status.model';

describe('ClosingAvalService', () => {
  let service: ClosingAvalService;
  let httpMock: HttpTestingController;

  const baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;
  const closingUrl = `${baseUrl}/v1/aval-closing`;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ClosingAvalService]
    });

    service = TestBed.inject(ClosingAvalService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getAllReportsDetailsAval', () => {
    it('should return the report list', () => {
      service.getAllReportsDetailsAval().subscribe(result => {
        expect(result.length).toBe(1);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-aval-details-reports`)
        .flush({ bodyResponse: [{ status: 'PENDIENTE' }] });
    });

    it('should return an empty array when the body is null', () => {
      service.getAllReportsDetailsAval().subscribe(result => {
        expect(result).toEqual([]);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-aval-details-reports`)
        .flush({ bodyResponse: null });
    });

    it('should return an empty array on a 400 with no records', () => {
      service.getAllReportsDetailsAval().subscribe(result => {
        expect(result).toEqual([]);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-aval-details-reports`).flush(
        { message: 'No registros para consultar' },
        { status: 400, statusText: 'Bad Request' }
      );
    });

    it('should rethrow any other error', () => {
      service.getAllReportsDetailsAval().subscribe({
        next: () => fail('should not emit'),
        error: (error: HttpErrorResponse) => {
          expect(error.status).toBe(500);
        }
      });

      httpMock.expectOne(`${baseUrl}/v1/all-aval-details-reports`).flush(
        { message: 'boom' },
        { status: 500, statusText: 'Server Error' }
      );
    });
  });

  describe('#updateReportsAval', () => {
    it('should PUT the pending mark request', () => {
      service.updateReportsAval().subscribe(response => {
        expect(response.bodyResponse).toContain('Actualización');
      });

      const request = httpMock.expectOne(`${baseUrl}/v1/update-aval-report`);
      expect(request.request.method).toBe('PUT');
      request.flush('Actualización completada, filas afectadas: 1');
    });
  });

  describe('#getAllReportsSeatAval', () => {
    it('should return the seat report list', () => {
      service.getAllReportsSeatAval().subscribe(result => {
        expect(result.length).toBe(1);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-seat-aval-details-reports`)
        .flush({ bodyResponse: [{ status: 'PROCESADO' }] });
    });

    it('should return an empty array when the body is null', () => {
      service.getAllReportsSeatAval().subscribe(result => {
        expect(result).toEqual([]);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-seat-aval-details-reports`)
        .flush({ bodyResponse: null });
    });
  });

  describe('#updateReportsSeatAval', () => {
    it('should PUT the seat pending mark request', () => {
      service.updateReportsSeatAval().subscribe(response => {
        expect(response.bodyResponse).toContain('Actualización');
      });

      const request = httpMock.expectOne(
        `${baseUrl}/v1/update-seat-aval-report`);
      expect(request.request.method).toBe('PUT');
      request.flush('Actualización completada, filas afectadas: 1');
    });
  });

  describe('#generateAccountingEntries', () => {
    it('should PUT the accounting generation request', () => {
      service.generateAccountingEntries().subscribe(response => {
        expect(response.bodyResponse?.period).toBe('202608');
      });

      const request = httpMock.expectOne(`${closingUrl}/generate`);
      expect(request.request.method).toBe('PUT');
      expect(request.request.body).toBeNull();
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush({
        bodyResponse: {
          message: 'Asientos generados con éxito.',
          period: '202608',
          files: []
        }
      });
    });
  });

  describe('#findGeneratedFiles', () => {
    it('should GET the generated files', () => {
      const files: IColombiaXmlFile[] = [{
        id: 1,
        period: '202608',
        family: 'ReasegAlfa',
        movementType: 'Constitucion',
        fileName: 'archivo.xml',
        lineCount: 4,
        processDate: '28/08/2026 10:00:00 a. m.',
        status: 'GENERADO'
      }];

      service.findGeneratedFiles().subscribe(response => {
        expect(response.bodyResponse?.[0].family).toBe('ReasegAlfa');
      });

      const request = httpMock.expectOne(`${closingUrl}/files`);
      expect(request.request.method).toBe('GET');
      request.flush({ bodyResponse: files });
    });
  });

  describe('#downloadXmlFile', () => {
    it('should GET the XML file as Blob', () => {
      const mockBlob = new Blob(['<SSC/>'], { type: 'application/xml' });

      service.downloadXmlFile(5).subscribe(response => {
        expect(response.body).toEqual(mockBlob);
      });

      const request = httpMock.expectOne(`${closingUrl}/files/5/download`);
      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expect(request.request.headers.get('Accept')).toBe('application/xml');

      request.flush(mockBlob, { status: 200, statusText: 'OK' });
    });
  });

  describe('#findReportStatus', () => {
    it('should GET the report status', () => {
      const status: IAvalReportStatus = {
        generationDate: '28/08/2026 10:00:00 a. m.',
        pendingMovements: 93
      };

      service.findReportStatus().subscribe(response => {
        expect(response.bodyResponse?.pendingMovements).toBe(93);
      });

      const request = httpMock.expectOne(`${closingUrl}/report/status`);
      expect(request.request.method).toBe('GET');
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');

      request.flush({ bodyResponse: status });
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

      service.downloadAvalReport().subscribe(response => {
        expect(response.body).toEqual(mockBlob);
        expect(response.headers.get('Content-Disposition'))
          .toContain('RPT_CIERRE_AVAL.xlsx');
      });

      const request = httpMock.expectOne(`${closingUrl}/report/download`);
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
});
