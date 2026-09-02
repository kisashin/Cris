import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';

import { AccountingEntryService } from './accounting-entry.service';
import { environment } from '../../../../../environments/environment';

describe('AccountingEntryService', () => {

  let service: AccountingEntryService;
  let httpMock: HttpTestingController;

  const url = `${environment.urlAPICierresBackEnd}/v1/claim-accounting`;

  const request = {
    product: '2012',
    comment: '2012_202602'
  };

  beforeEach(() => {

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AccountingEntryService]
    });

    service = TestBed.inject(AccountingEntryService);
    httpMock = TestBed.inject(HttpTestingController);

  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should query the accounting date', () => {

    service.getAccountingDate().subscribe(response => {
      expect(response.bodyResponse.accountingDate).toBe('20260201');
    });

    const req = httpMock.expectOne(`${url}/accounting-date`);

    expect(req.request.method).toBe('GET');

    req.flush({ bodyResponse: { accountingDate: '20260201' } });

  });

  it('should query the products', () => {

    service.getProducts().subscribe(response => {
      expect(response.bodyResponse.length).toBe(1);
    });

    const req = httpMock.expectOne(`${url}/products`);

    expect(req.request.method).toBe('GET');

    req.flush({ bodyResponse: [{ product: '2012' }] });

  });

  it('should send the file as multipart', () => {

    const file = new File(['contenido'], '326CO21SR0122026090110.csv', {
      type: 'text/csv'
    });

    service.loadClaims(file, '2012', 'j36147').subscribe(response => {
      expect(response.bodyResponse.totalRows).toBe(5);
    });

    const req = httpMock.expectOne(`${url}/load`);

    expect(req.request.method).toBe('POST');
    expect(req.request.body instanceof FormData).toBeTrue();

    const body = req.request.body as FormData;

    expect((body.get('file') as File).name).toBe('326CO21SR0122026090110.csv');
    expect(body.get('product')).toBe('2012');
    expect(body.get('user')).toBe('j36147');

    req.flush({
      bodyResponse: {
        message: '5 Registros Cargados',
        totalRows: 5,
        incompleteRows: 0
      }
    });

  });

  it('should not set the content type on the upload', () => {

    const file = new File(['contenido'], 'archivo.csv', { type: 'text/csv' });

    service.loadClaims(file, '2012', 'j36147').subscribe();

    const req = httpMock.expectOne(`${url}/load`);

    expect(req.request.headers.get('Content-Type')).toBeNull();

    req.flush({ bodyResponse: {} });

  });

  it('should request the entry preview', () => {

    service.previewAccountingEntry(request).subscribe(response => {
      expect(response.bodyResponse.length).toBe(1);
    });

    const req = httpMock.expectOne(`${url}/generate`);

    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(request);

    req.flush({ bodyResponse: [{ journalType: 'SINIE' }] });

  });

  it('should register the entry', () => {

    service.registerAccountingEntry(request).subscribe(response => {
      expect(response.bodyResponse).toBeNull();
    });

    const req = httpMock.expectOne(`${url}/register`);

    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(request);

    req.flush({ bodyResponse: null });

  });

  it('should query the account summary', () => {

    service.getAccountSummary(request).subscribe(response => {
      expect(response.bodyResponse.length).toBe(1);
    });

    const req = httpMock.expectOne(`${url}/total-by-account`);

    expect(req.request.method).toBe('POST');

    req.flush({ bodyResponse: [{ product: '2012' }] });

  });

  it('should send the entry with the user', () => {

    const sendRequest = {
      product: '2012',
      comment: '2012_202602',
      user: 'j36147'
    };

    service.sendAccountingEntry(sendRequest).subscribe(response => {
      expect(response.bodyResponse.files.length).toBe(3);
    });

    const req = httpMock.expectOne(`${url}/send`);

    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(sendRequest);

    req.flush({
      bodyResponse: {
        files: ['a.XML', 'b.XML', 'c.XML'],
        message: 'Interfaz generada correctamente.'
      }
    });

  });

  it('should query the generated files', () => {

    service.getFiles().subscribe(response => {
      expect(response.bodyResponse.length).toBe(1);
    });

    const req = httpMock.expectOne(`${url}/files`);

    expect(req.request.method).toBe('GET');

    req.flush({
      bodyResponse: [
        {
          id: 1,
          product: '2012',
          journalType: 'SINIE',
          fileName: 'archivo.XML',
          generationDate: '02/09/2026 03:04:45'
        }
      ]
    });

  });

  it('should download the file as a blob', () => {

    service.downloadFile(1).subscribe(response => {
      expect(response.body?.size).toBeGreaterThan(0);
    });

    const req = httpMock.expectOne(`${url}/files/1/download`);

    expect(req.request.method).toBe('GET');
    expect(req.request.responseType).toBe('blob');

    req.flush(new Blob(['<SSC/>'], { type: 'application/xml' }));

  });

});
