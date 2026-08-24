import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { NO_ERRORS_SCHEMA } from '@angular/core';
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
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    fixture = TestBed.createComponent(AccountingClosingCAComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should build one row per generated file', () => {
    service.generateAccountingEntries.and.returnValue(
      of({ bodyResponse: result } as any)
    );

    component.generateAccountingEntries();

    expect(component.dataSource.length).toBe(1);
    expect(component.dataSource[0].movementType).toBe('Pago');
    expect(component.dataSource[0].processDate).toBe(result.processDate);
    expect(component.dataSource[0].status).toBe('PROCESADO');
    expect(component.dataSource[0].action).toBe('Descargar XML');
    expect(component.isGenerating).toBeFalse();
    expect(toastr.success).toHaveBeenCalledWith(result.message);
  });

  it('should leave the table empty when there are no files', () => {
    service.generateAccountingEntries.and.returnValue(
      of({ bodyResponse: { ...result, files: [] } } as any)
    );

    component.generateAccountingEntries();

    expect(component.dataSource).toEqual([]);
  });

  it('should not launch a second generation while one is running', () => {
    component.isGenerating = true;

    component.generateAccountingEntries();

    expect(service.generateAccountingEntries).not.toHaveBeenCalled();
  });

  it('should clear the table when the generation fails', () => {
    component.dataSource = [{ movementType: 'Pago' }];
    service.generateAccountingEntries.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.generateAccountingEntries();

    expect(component.dataSource).toEqual([]);
    expect(component.isGenerating).toBeFalse();
    expect(toastr.error).toHaveBeenCalled();
  });

  it('should download the XML of the selected row', () => {
    const anchor = document.createElement('a');
    spyOn(document, 'createElement').and.returnValue(anchor);
    spyOn(anchor, 'click');
    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:xml');
    spyOn(window.URL, 'revokeObjectURL');

    component.onDownloadXml({ file: result.files[0] });

    expect(anchor.download).toBe(result.files[0].fileName);
    expect(anchor.click).toHaveBeenCalled();
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:xml');
  });

  it('should warn when the selected row has no content', () => {
    component.onDownloadXml({ file: null });

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
