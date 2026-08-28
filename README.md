import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { AccountingClosingCAComponent } from './accounting-closing-ca.component';
import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';
import { IAccountingXmlFile } from '../../models/center-accounting-result.model';

describe('AccountingClosingCAComponent', () => {
  let component: AccountingClosingCAComponent;
  let fixture: ComponentFixture<AccountingClosingCAComponent>;
  let caService: jasmine.SpyObj<AccountingClosingCaService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const file: IAccountingXmlFile = {
    id: 1,
    period: '202608',
    movementType: 'Pago',
    fileName: 'Sinie_ReasegCentro_Pago20260824.xml',
    lineCount: 216,
    processDate: '25/08/2026 03:45:30 p. m.',
    status: 'GENERADO'
  };

  const stubAnchor = (): HTMLAnchorElement => {
    const anchor = document.createElement('a');
    spyOn(document, 'createElement').and.returnValue(anchor);
    spyOn(anchor, 'click');
    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
    spyOn(window.URL, 'revokeObjectURL');
    return anchor;
  };

  beforeEach(async () => {
    caService = jasmine.createSpyObj('AccountingClosingCaService', [
      'findGeneratedFiles',
      'generateAccountingEntries',
      'downloadXmlFile',
      'downloadMovementsReport'
    ]);
    dialog = jasmine.createSpyObj('MatDialog', ['open']);
    toastr = jasmine.createSpyObj('ToastrService', [
      'success', 'error', 'warning'
    ]);

    caService.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [file] } as any));

    await TestBed.configureTestingModule({
      imports: [AccountingClosingCAComponent, NoopAnimationsModule],
      providers: [
        { provide: AccountingClosingCaService, useValue: caService },
        { provide: MatDialog, useValue: dialog },
        { provide: ToastrService, useValue: toastr }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AccountingClosingCAComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#loadGeneratedFiles', () => {
    it('should load the generated files on init', () => {
      expect(component.dataSource.length).toBe(1);
      expect(component.dataSource[0].movementType).toBe('Pago');
      expect(component.isLoading).toBeFalse();
    });

    it('should use an empty list when the body is null', () => {
      caService.findGeneratedFiles.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
    });

    it('should clear the list when the request fails', () => {
      caService.findGeneratedFiles.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
      expect(component.isLoading).toBeFalse();
    });
  });

  describe('#generateAccountingEntries', () => {
    it('should generate when the dialog is confirmed', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      caService.generateAccountingEntries.and.returnValue(of({
        bodyResponse: { message: 'Asientos generados con éxito.' }
      } as any));

      component.generateAccountingEntries();

      expect(caService.generateAccountingEntries).toHaveBeenCalled();
      expect(toastr.success)
        .toHaveBeenCalledWith('Asientos generados con éxito.');
      expect(component.isGenerating).toBeFalse();
    });

    it('should show a default message when the body has none', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      caService.generateAccountingEntries.and.returnValue(
        of({ bodyResponse: null } as any));

      component.generateAccountingEntries();

      expect(toastr.success)
        .toHaveBeenCalledWith('Proceso ejecutado correctamente.');
    });

    it('should not generate when the dialog is cancelled', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

      component.generateAccountingEntries();

      expect(caService.generateAccountingEntries).not.toHaveBeenCalled();
    });

    it('should ignore the click while a generation is running', () => {
      component.isGenerating = true;

      component.generateAccountingEntries();

      expect(dialog.open).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      caService.generateAccountingEntries.and.returnValue(
        throwError(() => ({
          error: { errorHeader: { errorMessage: 'Error controlado' } }
        })));

      component.generateAccountingEntries();

      expect(toastr.error).toHaveBeenCalledWith('Error controlado');
      expect(component.isGenerating).toBeFalse();
    });

    it('should show a default error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      caService.generateAccountingEntries.and.returnValue(
        throwError(() => new Error('boom')));

      component.generateAccountingEntries();

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible generar los asientos contables.');
    });
  });

  describe('#onDownloadXml', () => {
    it('should download the file', () => {
      caService.downloadXmlFile.and.returnValue(of(new HttpResponse({
        body: new Blob(['<SSC/>'], { type: 'application/xml' }),
        status: 200
      })));

      const anchor = stubAnchor();

      component.onDownloadXml(file);

      expect(caService.downloadXmlFile).toHaveBeenCalledWith(1);
      expect(anchor.download)
        .toBe('Sinie_ReasegCentro_Pago20260824.xml');
      expect(anchor.click).toHaveBeenCalled();
      expect(window.URL.revokeObjectURL).toHaveBeenCalled();
    });

    it('should warn when the file is empty', () => {
      caService.downloadXmlFile.and.returnValue(
        of(new HttpResponse({ body: new Blob([]), status: 200 })));

      component.onDownloadXml(file);

      expect(toastr.warning)
        .toHaveBeenCalledWith('El archivo generado no contiene información.');
    });

    it('should warn when the body is null', () => {
      caService.downloadXmlFile.and.returnValue(
        of(new HttpResponse<Blob>({ body: null, status: 200 })));

      component.onDownloadXml(file);

      expect(toastr.warning).toHaveBeenCalled();
    });

    it('should show an error when the download fails', () => {
      caService.downloadXmlFile.and.returnValue(
        throwError(() => new Error('boom')));

      component.onDownloadXml(file);

      expect(toastr.error)
        .toHaveBeenCalledWith('No fue posible descargar el archivo XML.');
    });
  });

  describe('#downloadReport', () => {
    it('should use the file name from the Content-Disposition header', () => {
      caService.downloadMovementsReport.and.returnValue(
        of(new HttpResponse({
          body: new Blob(['excel']),
          headers: new HttpHeaders({
            'Content-Disposition':
              'attachment; filename="ReporteMovimientosCentro.xlsx"'
          }),
          status: 200
        })));

      const anchor = stubAnchor();

      component.downloadReport();

      expect(anchor.download).toBe('ReporteMovimientosCentro.xlsx');
      expect(component.isDownloading).toBeFalse();
    });

    it('should fall back to the default file name', () => {
      caService.downloadMovementsReport.and.returnValue(
        of(new HttpResponse({
          body: new Blob(['excel']),
          status: 200
        })));

      const anchor = stubAnchor();

      component.downloadReport();

      expect(anchor.download).toBe('ReporteMovimientosCentro.xlsx');
    });

    it('should ignore the click while a download is running', () => {
      component.isDownloading = true;

      component.downloadReport();

      expect(caService.downloadMovementsReport).not.toHaveBeenCalled();
    });

    it('should warn when the report is empty', () => {
      caService.downloadMovementsReport.and.returnValue(
        of(new HttpResponse({ body: new Blob([]), status: 200 })));

      component.downloadReport();

      expect(toastr.warning)
        .toHaveBeenCalledWith('El archivo generado no contiene información.');
    });

    it('should show an error when the download fails', () => {
      caService.downloadMovementsReport.and.returnValue(
        throwError(() => new Error('boom')));

      component.downloadReport();

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible descargar el reporte de movimientos.');
      expect(component.isDownloading).toBeFalse();
    });
  });
});
