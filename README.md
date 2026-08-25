import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { AccountingClosingCAComponent } from './accounting-closing-ca.component';
import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';
import { IAccountingXmlFile } from '../../models/center-accounting-result.model';

describe('AccountingClosingCAComponent', () => {
  let component: AccountingClosingCAComponent;
  let fixture: ComponentFixture<AccountingClosingCAComponent>;
  let service: jasmine.SpyObj<AccountingClosingCaService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const xmlFile: IAccountingXmlFile = {
    id: 1,
    period: '202608',
    movementType: 'Pago',
    fileName: 'Sinie_ReasegCentro_Pago20260824.xml',
    lineCount: 2,
    processDate: '24/08/2026 03:03:29 PM',
    status: 'GENERADO'
  };

  const blobResponse = (body: Blob, disposition?: string) =>
    new HttpResponse<Blob>({
      body,
      headers: disposition
        ? new HttpHeaders({ 'Content-Disposition': disposition })
        : new HttpHeaders()
    });

  const mockAnchor = () => {
    const anchor = document.createElement('a');
    spyOn(document, 'createElement').and.returnValue(anchor);
    spyOn(anchor, 'click');
    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:test');
    spyOn(window.URL, 'revokeObjectURL');
    return anchor;
  };

  const mockDialogResult = (confirmed: boolean) => {
    dialog.open.and.returnValue({
      afterClosed: () => of(confirmed)
    } as any);
  };

  beforeEach(async () => {
    service = jasmine.createSpyObj('AccountingClosingCaService', [
      'generateAccountingEntries',
      'findGeneratedFiles',
      'downloadXmlFile',
      'downloadMovementsReport'
    ]);

    dialog = jasmine.createSpyObj('MatDialog', ['open']);

    toastr = jasmine.createSpyObj('ToastrService', [
      'success',
      'error',
      'warning'
    ]);

    await TestBed.configureTestingModule({
      imports: [AccountingClosingCAComponent],
      providers: [
        { provide: AccountingClosingCaService, useValue: service },
        { provide: MatDialog, useValue: dialog },
        { provide: ToastrService, useValue: toastr }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AccountingClosingCAComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load the generated files on init', () => {
    service.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [xmlFile] } as any)
    );

    component.ngOnInit();

    expect(component.dataSource).toEqual([xmlFile]);
    expect(component.isLoading).toBeFalse();
  });

  it('should leave the table empty when there is no history', () => {
    service.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: null } as any)
    );

    component.loadGeneratedFiles();

    expect(component.dataSource).toEqual([]);
  });

  it('should clear the table when the history query fails', () => {
    component.dataSource = [xmlFile];
    service.findGeneratedFiles.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.loadGeneratedFiles();

    expect(component.dataSource).toEqual([]);
    expect(component.isLoading).toBeFalse();
  });

  it('should ask for confirmation before generating', () => {
    mockDialogResult(false);

    component.generateAccountingEntries();

    expect(dialog.open).toHaveBeenCalled();
    expect(service.generateAccountingEntries).not.toHaveBeenCalled();
    expect(component.isGenerating).toBeFalse();
  });

  it('should generate and reload the table when confirmed', () => {
    mockDialogResult(true);
    service.generateAccountingEntries.and.returnValue(
      of({ bodyResponse: { message: 'OK', period: '202608', files: [] } } as any)
    );
    service.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [xmlFile] } as any)
    );

    component.generateAccountingEntries();

    expect(service.generateAccountingEntries).toHaveBeenCalled();
    expect(toastr.success).toHaveBeenCalledWith('OK');
    expect(component.isGenerating).toBeFalse();
    expect(component.dataSource).toEqual([xmlFile]);
  });

  it('should not open the dialog while a generation is running', () => {
    component.isGenerating = true;

    component.generateAccountingEntries();

    expect(dialog.open).not.toHaveBeenCalled();
  });

  it('should show the backend message and reload when generation fails', () => {
    mockDialogResult(true);
    service.generateAccountingEntries.and.returnValue(
      throwError(() => ({
        error: { errorHeader: { errorMessage: 'Sin movimientos' } }
      }))
    );
    service.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [xmlFile] } as any)
    );

    component.generateAccountingEntries();

    expect(toastr.error).toHaveBeenCalledWith('Sin movimientos');
    expect(component.isGenerating).toBeFalse();
    expect(component.dataSource).toEqual([xmlFile]);
  });

  it('should show a default message when the error has no body', () => {
    mockDialogResult(true);
    service.generateAccountingEntries.and.returnValue(
      throwError(() => new Error('error'))
    );
    service.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [] } as any)
    );

    component.generateAccountingEntries();

    expect(toastr.error).toHaveBeenCalledWith(
      'No fue posible generar los asientos contables.'
    );
  });

  it('should download the XML of the selected row', () => {
    const anchor = mockAnchor();
    service.downloadXmlFile.and.returnValue(
      of(blobResponse(new Blob(['<SSC/>'])))
    );

    component.onDownloadXml(xmlFile);

    expect(service.downloadXmlFile).toHaveBeenCalledWith(1);
    expect(anchor.download).toBe(xmlFile.fileName);
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:test');
  });

  it('should warn when the XML has no content', () => {
    service.downloadXmlFile.and.returnValue(
      of(blobResponse(new Blob([])))
    );

    component.onDownloadXml(xmlFile);

    expect(toastr.warning).toHaveBeenCalled();
  });

  it('should show an error when the XML download fails', () => {
    service.downloadXmlFile.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.onDownloadXml(xmlFile);

    expect(toastr.error).toHaveBeenCalledWith(
      'No fue posible descargar el archivo XML.'
    );
  });

  it('should download the Excel report using the response file name', () => {
    const anchor = mockAnchor();
    service.downloadMovementsReport.and.returnValue(
      of(blobResponse(
        new Blob(['data']),
        'attachment; filename="Reporte.xlsx"'))
    );

    component.downloadReport();

    expect(anchor.download).toBe('Reporte.xlsx');
    expect(component.isDownloading).toBeFalse();
  });

  it('should fall back to the default Excel file name', () => {
    const anchor = mockAnchor();
    service.downloadMovementsReport.and.returnValue(
      of(blobResponse(new Blob(['data'])))
    );

    component.downloadReport();

    expect(anchor.download).toBe('ReporteMovimientosCentro.xlsx');
  });

  it('should not launch a second Excel download while one is running', () => {
    component.isDownloading = true;

    component.downloadReport();

    expect(service.downloadMovementsReport).not.toHaveBeenCalled();
  });

  it('should warn when the Excel report is empty', () => {
    service.downloadMovementsReport.and.returnValue(
      of(blobResponse(new Blob([])))
    );

    component.downloadReport();

    expect(toastr.warning).toHaveBeenCalled();
    expect(component.isDownloading).toBeFalse();
  });

  it('should show an error when the Excel download fails', () => {
    service.downloadMovementsReport.and.returnValue(
      throwError(() => new Error('error'))
    );

    component.downloadReport();

    expect(component.isDownloading).toBeFalse();
    expect(toastr.error).toHaveBeenCalledWith(
      'No fue posible descargar el reporte de movimientos.'
    );
  });
});
