import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { AccountingClosingCaService } from './accounting-closing-ca.service';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import {
  IAccountingXmlFile,
  ICenterAccountingResult
} from '../models/center-accounting-result.model';

describe('AccountingClosingCaService', () => {
  let service: AccountingClosingCaService;
  let httpMock: HttpTestingController;

  const baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/cardif-center-closing`;

  const expectTraceHeaders = (request: any, accept: string): void => {
    expect(request.request.headers.has('correlation_id')).toBeTrue();
    expect(request.request.headers.has('request_id')).toBeTrue();
    expect(request.request.headers.has('_p')).toBeTrue();
    expect(request.request.headers.get('Accept')).toBe(accept);
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AccountingClosingCaService]
    });

    service = TestBed.inject(AccountingClosingCaService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#generateAccountingEntries', () => {
    it('should PUT the accounting generation request', () => {
      const mockResponse: INewGeneralResponse<ICenterAccountingResult> = {
        correlationId: 'correlation-id',
        responseHeader: {
          returnCode: 200,
          message: 'Success'
        },
        bodyResponse: {
          message: 'Asientos generados con éxito.',
          period: '202608',
          files: []
        }
      };

      service.generateAccountingEntries().subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      const request = httpMock.expectOne(`${baseUrl}/generate`);
      expect(request.request.method).toBe('PUT');
      expect(request.request.body).toBeNull();
      expectTraceHeaders(request, 'application/json');

      request.flush(mockResponse);
    });
  });

  describe('#findGeneratedFiles', () => {
    it('should GET the generated files', () => {
      const files: IAccountingXmlFile[] = [{
        id: 1,
        period: '202608',
        movementType: 'Pago',
        fileName: 'archivo.xml',
        lineCount: 4,
        processDate: '24/08/2026 03:45:30 p. m.',
        status: 'GENERADO'
      }];

      const mockResponse: INewGeneralResponse<IAccountingXmlFile[]> = {
        correlationId: 'correlation-id',
        responseHeader: {
          returnCode: 200,
          message: 'Success'
        },
        bodyResponse: files
      };

      service.findGeneratedFiles().subscribe(response => {
        expect(response.bodyResponse?.length).toBe(1);
        expect(response.bodyResponse?.[0].fileName).toBe('archivo.xml');
      });

      const request = httpMock.expectOne(`${baseUrl}/files`);
      expect(request.request.method).toBe('GET');
      expectTraceHeaders(request, 'application/json');

      request.flush(mockResponse);
    });
  });

  describe('#downloadXmlFile', () => {
    it('should GET the XML file as Blob', () => {
      const mockBlob = new Blob(['<SSC/>'], { type: 'application/xml' });
      const responseHeaders = new HttpHeaders({
        'Content-Disposition': 'attachment; filename="archivo.xml"'
      });

      service.downloadXmlFile(7).subscribe(response => {
        expect(response.body).toEqual(mockBlob);
        expect(response.headers.get('Content-Disposition'))
          .toContain('archivo.xml');
      });

      const request = httpMock.expectOne(`${baseUrl}/files/7/download`);
      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expectTraceHeaders(request, 'application/xml');

      request.flush(mockBlob, {
        headers: responseHeaders,
        status: 200,
        statusText: 'OK'
      });
    });
  });

  describe('#downloadMovementsReport', () => {
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
          'attachment; filename="ReporteMovimientosCentro.xlsx"'
      });

      service.downloadMovementsReport().subscribe(response => {
        expect(response.body).toEqual(mockBlob);
        expect(
          response.headers.get('Content-Disposition')
        ).toContain('ReporteMovimientosCentro.xlsx');
      });

      const request = httpMock.expectOne(`${baseUrl}/download`);
      expect(request.request.method).toBe('GET');
      expect(request.request.responseType).toBe('blob');
      expectTraceHeaders(
        request,
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
