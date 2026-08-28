import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ClosingCardifService } from './closing-cardif.service';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { IColombiaXmlFile } from '../models/colombia-accounting-result.model';

describe('ClosingCardifService', () => {
  let service: ClosingCardifService;
  let httpMock: HttpTestingController;

  const baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;
  const closingUrl = `${baseUrl}/v1/cardif-closing`;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ClosingCardifService]
    });

    service = TestBed.inject(ClosingCardifService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getAllReportsDetailsCardif', () => {
    it('should return the report list', () => {
      const mockResponse = {
        bodyResponse: [{ dateProcessing: '2026-08-24', status: 'PROCESADO' }]
      } as INewGeneralResponse<any>;

      service.getAllReportsDetailsCardif().subscribe(result => {
        expect(result.length).toBe(1);
      });

      const request = httpMock.expectOne(`${baseUrl}/v1/all-cardif-reports`);
      expect(request.request.method).toBe('GET');
      request.flush(mockResponse);
    });

    it('should return an empty array when the body is null', () => {
      service.getAllReportsDetailsCardif().subscribe(result => {
        expect(result).toEqual([]);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-cardif-reports`)
        .flush({ bodyResponse: null });
    });

    it('should return an empty array on a 400 with no records', () => {
      service.getAllReportsDetailsCardif().subscribe(result => {
        expect(result).toEqual([]);
      });

      httpMock.expectOne(`${baseUrl}/v1/all-cardif-reports`).flush(
        { errorDetail: { message: 'No registros para consultar' } },
        { status: 400, statusText: 'Bad Request' }
      );
    });

    it('should rethrow any other error', () => {
      service.getAllReportsDetailsCardif().subscribe({
        next: () => fail('should not emit'),
        error: (error: HttpErrorResponse) => {
          expect(error.status).toBe(500);
        }
      });

      httpMock.expectOne(`${baseUrl}/v1/all-cardif-reports`).flush(
        { message: 'boom' },
        { status: 500, statusText: 'Server Error' }
      );
    });
  });

  describe('#updateReportsCardif', () => {
    it('should PUT the pending mark request', () => {
      service.updateReportsCardif().subscribe(response => {
        expect(response.bodyResponse).toContain('Actualización');
      });

      const request = httpMock.expectOne(
        `${baseUrl}/v1/update-cardif-report`);
      expect(request.request.method).toBe('PUT');
      request.flush('Actualización completada, filas afectadas: 1');
    });
  });

  describe('#generateAccountingEntries', () => {
    it('should PUT the accounting generation request', () => {
      const mockResponse = {
        bodyResponse: {
          message: 'Asientos generados con éxito.',
          period: '202608',
          files: []
        }
      } as INewGeneralResponse<any>;

      service.generateAccountingEntries().subscribe(response => {
        expect(response.bodyResponse?.message)
          .toBe('Asientos generados con éxito.');
      });

      const request = httpMock.expectOne(`${closingUrl}/generate`);
      expect(request.request.method).toBe('PUT');
      expect(request.request.body).toBeNull();
      expect(request.request.headers.get('Accept'))
        .toBe('application/json');
      request.flush(mockResponse);
    });
  });

  describe('#findGeneratedFiles', () => {
    it('should GET the generated files', () => {
      const files: IColombiaXmlFile[] = [{
        id: 1,
        period: '202608',
        family: 'ReasegCardif',
        movementType: 'Pago',
        fileName: 'archivo.xml',
        lineCount: 4,
        processDate: '28/08/2026 10:00:00 a. m.',
        status: 'GENERADO'
      }];

      service.findGeneratedFiles().subscribe(response => {
        expect(response.bodyResponse?.[0].family).toBe('ReasegCardif');
      });

      const request = httpMock.expectOne(`${closingUrl}/files`);
      expect(request.request.method).toBe('GET');
      request.flush({ bodyResponse: files });
    });
  });

  describe('#downloadXmlFile', () => {
    it('should GET the XML file as Blob', () => {
      const mockBlob = new Blob(['<SSC/>'], { type: 'application/xml' });
      const responseHeaders = new HttpHeaders({
        'Content-Disposition': 'attachment; filename="archivo.xml"'
      });

      service.downloadXmlFile(3).subscribe(response => {
        expect(response.body).toEqual(mockBlob);
      });

      const request = httpMock.expectOne(`${closingUrl}/files/3/download`);
      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expect(request.request.headers.get('Accept')).toBe('application/xml');

      request.flush(mockBlob, {
        headers: responseHeaders,
        status: 200,
        statusText: 'OK'
      });
    });
  });
});
