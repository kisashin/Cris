import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpResponse, HttpHeaders } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { AccountingClosingCAComponent } from './accounting-closing-ca.component';
import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';
import { ICenterAccountingResult } from '../../models/center-accounting-result.model';

describe('AccountingClosingCAComponent', () => {
  let component: AccountingClosingCAComponent;
  let fixture: ComponentFixture<AccountingClosingCAComponent>;
  let service: jasmine.SpyObj<AccountingClosingCaService>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const result: ICenterAccountingResult = {
    message: 'Asientos generados con éxito.',
    processDate: '24/08/2026 03:03:29 p. m.',
    status: 'PROCESADO',
    period: '202608',
    files: [
      {
        movementType: 'Pago',
        fileName: 'Sinie_ReasegCentro_Pago20260824.xml',
        lineCount: 2,
        content: btoa('<SSC/>')
      }
    ]
  };

  beforeEach(async () => {
    service = jasmine.createSpyObj('AccountingClosingCaService', [
      'generateAccountingEntries',
      'downloadMovementsReport'
    ]);

    toastr = jasmine.createSpyObj('ToastrService', [
      'success',
      'error',
      'warning'
    ]);

    await TestBed.configureTestingModule({
      imports: [AccountingClosingCAComponent],
      providers: [
        { provide: AccountingClosingCaService, useValue: service },
        { provide: ToastrService, useValue: toastr }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AccountingClosingCAComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should store the generated files and show the success message', () => {
    service.generateAccountingEntries.and.returnValue(
      of({ bodyResponse: result } as any)
    );

    component.generateAccountingEntries();

    expect(component.result).toEqual(result);
    expect(component.isGenerating).toBeFalse();
    expect(toastr.success).toHaveBeenCalledWith(result.message);
  });

  it('should not launch a second generation while one is running', () => {
    component.isGenerating = true;

    component.generateAccountingEntries();

    expect(service.generateAccountingEntries).not.toHaveBeenCalled();
  });

  it('should clear the result when the generation fails', () => {
    component.result = result;
    service.generateAccountingEntries.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.generateAccountingEntries();

    expect(component.result).toBeNull();
    expect(component.isGenerating).toBeFalse();
    expect(toastr.error).toHaveBeenCalled();
  });

  it('should download the XML file of a movement type', () => {
    const anchor = document.createElement('a');
    spyOn(document, 'createElement').and.returnValue(anchor);
    spyOn(anchor, 'click');
    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:xml');
    spyOn(window.URL, 'revokeObjectURL');

    component.downloadXmlFile(result.files[0]);

    expect(anchor.download).toBe(result.files[0].fileName);
    expect(anchor.click).toHaveBeenCalled();
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:xml');
  });

  it('should warn when the XML file has no content', () => {
    component.downloadXmlFile({
      movementType: 'Pago',
      fileName: 'Sinie_ReasegCentro_Pago20260824.xml',
      lineCount: 0,
      content: ''
    });

    expect(toastr.warning).toHaveBeenCalled();
  });

  it('should download the Excel report', () => {
    const anchor = document.createElement('a');
    spyOn(document, 'createElement').and.returnValue(anchor);
    spyOn(anchor, 'click');
    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:xlsx');
    spyOn(window.URL, 'revokeObjectURL');

    const response = new HttpResponse<Blob>({
      body: new Blob(['data']),
      headers: new HttpHeaders({
        'Content-Disposition': 'attachment; filename="Reporte.xlsx"'
      })
    });

    service.downloadMovementsReport.and.returnValue(of(response));

    component.downloadReport();

    expect(anchor.download).toBe('Reporte.xlsx');
    expect(component.isDownloading).toBeFalse();
    expect(toastr.success).toHaveBeenCalled();
  });

  it('should warn when the Excel report is empty', () => {
    const response = new HttpResponse<Blob>({
      body: new Blob([]),
      headers: new HttpHeaders()
    });

    service.downloadMovementsReport.and.returnValue(of(response));

    component.downloadReport();

    expect(toastr.warning).toHaveBeenCalled();
  });

  it('should show an error when the Excel download fails', () => {
    service.downloadMovementsReport.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.downloadReport();

    expect(component.isDownloading).toBeFalse();
    expect(toastr.error).toHaveBeenCalled();
  });
});
