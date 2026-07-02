accounting-closing-ca.service.spec.ts



import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpHeaders } from '@angular/common/http';

import { environment } from 'src/environments/environment';
import { AccountingClosingCaService } from './accounting-closing-ca.service';
import { INewGeneralResponse } from '../../models/new-general-response.interface';

describe('AccountingClosingCaService', () => {
  let service: AccountingClosingCaService;
  let httpMock: HttpTestingController;

  const baseUrl =
    `${environment.urlAPIClosingClaimsBackEnd}/v1/cardif-center-closing`;

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
      const mockResponse: INewGeneralResponse<string> = {
        correlationId: 'correlation-id',
        responseHeader: {
          returnCode: 200,
          message: 'Success'
        },
        bodyResponse: 'Asientos generados con éxito.'
      };

      service.generateAccountingEntries().subscribe(response => {
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
