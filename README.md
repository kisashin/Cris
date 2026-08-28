import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { ClaimsClosingAvalComponent } from './claims-closing-aval.component';
import { ClosingAvalService } from '../../services/closing-aval.service';
import { IColombiaXmlFile } from '../../models/colombia-accounting-result.model';
import { IAvalReportStatus } from '../../models/aval-report-status.model';

describe('ClaimsClosingAvalComponent', () => {
  let component: ClaimsClosingAvalComponent;
  let fixture: ComponentFixture<ClaimsClosingAvalComponent>;
  let avalService: jasmine.SpyObj<ClosingAvalService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const file: IColombiaXmlFile = {
    id: 1,
    period: '202608',
    family: 'ReasegAlfa',
    movementType: 'Constitucion',
    fileName: 'archivo.xml',
    lineCount: 4,
    processDate: '28/08/2026 10:00:00 a. m.',
    status: 'GENERADO'
  };

  const status: IAvalReportStatus = {
    generationDate: '28/08/2026 10:00:00 a. m.',
    pendingMovements: 93
  };

  beforeEach(async () => {
    avalService = jasmine.createSpyObj('ClosingAvalService', [
      'findReportStatus',
      'downloadAvalReport',
      'findGeneratedFiles',
      'generateAccountingEntries',
      'downloadXmlFile'
    ]);
    dialog = jasmine.createSpyObj('MatDialog', ['open']);
    toastr = jasmine.createSpyObj('ToastrService', [
      'success', 'error', 'warning'
    ]);

    avalService.findReportStatus.and.returnValue(
      of({ bodyResponse: status } as any));
    avalService.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [file] } as any));

    await TestBed.configureTestingModule({
      imports: [ClaimsClosingAvalComponent, NoopAnimationsModule],
      providers: [
        { provide: ClosingAvalService, useValue: avalService },
        { provide: MatDialog, useValue: dialog },
        { provide: ToastrService, useValue: toastr }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ClaimsClosingAvalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#loadReportStatus', () => {
    it('should show the table when there are pending movements', () => {
      expect(component.hasAvalData).toBeTrue();
      expect(component.reportDataSource.length).toBe(1);
      expect(component.isLoadingReport).toBeFalse();
    });

    it('should hide the table when there are no pending movements', () => {
      avalService.findReportStatus.and.returnValue(of({
        bodyResponse: { generationDate: 'fecha', pendingMovements: 0 }
      } as any));

      component.loadReportStatus();

      expect(component.hasAvalData).toBeFalse();
      expect(component.reportDataSource).toEqual([]);
    });

    it('should hide the table when the body is null', () => {
      avalService.findReportStatus.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadReportStatus();

      expect(component.hasAvalData).toBeFalse();
      expect(component.reportDataSource).toEqual([]);
    });

    it('should hide the table when the request fails', () => {
      avalService.findReportStatus.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadReportStatus();

      expect(component.hasAvalData).toBeFalse();
      expect(component.isLoadingReport).toBeFalse();
    });
  });

  describe('#downloadReport', () => {
    it('should download the Excel report', () => {
      avalService.downloadAvalReport.and.returnValue(of(new HttpResponse({
        body: new Blob(['excel']),
        headers: undefined,
        status: 200
      })));

      const anchor = document.createElement('a');
      spyOn(document, 'createElement').and.returnValue(anchor);
      spyOn(anchor, 'click');
      spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
      spyOn(window.URL, 'revokeObjectURL');

      component.downloadReport();

      expect(anchor.download).toBe('RPT_CIERRE_AVAL.xlsx');
      expect(anchor.click).toHaveBeenCalled();
      expect(component.isDownloadingReport).toBeFalse();
    });

    it('should ignore the click while a download is running', () => {
      component.isDownloadingReport = true;

      component.downloadReport();

      expect(avalService.downloadAvalReport).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      avalService.downloadAvalReport.and.returnValue(throwError(() => ({
        error: { errorHeader: { errorMessage: 'Sin movimientos' } }
      })));

      component.downloadReport();

      expect(toastr.error).toHaveBeenCalledWith('Sin movimientos');
      expect(component.isDownloadingReport).toBeFalse();
    });

    it('should show a default error message', () => {
      avalService.downloadAvalReport.and.returnValue(
        throwError(() => new Error('boom')));

      component.downloadReport();

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible descargar el reporte de movimientos.');
    });
  });

  describe('#loadGeneratedFiles', () => {
    it('should load the generated files on init', () => {
      expect(component.dataSource.length).toBe(1);
      expect(component.isLoading).toBeFalse();
    });

    it('should use an empty list when the body is null', () => {
      avalService.findGeneratedFiles.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
    });

    it('should clear the list when the request fails', () => {
      avalService.findGeneratedFiles.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
    });
  });

  describe('#generateAccountingEntries', () => {
    it('should generate when the dialog is confirmed', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAccountingEntries.and.returnValue(of({
        bodyResponse: { message: 'Asientos generados con éxito.' }
      } as any));

      component.generateAccountingEntries();

      expect(toastr.success)
        .toHaveBeenCalledWith('Asientos generados con éxito.');
      expect(component.isGenerating).toBeFalse();
    });

    it('should show a default message when the body has none', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAccountingEntries.and.returnValue(
        of({ bodyResponse: null } as any));

      component.generateAccountingEntries();

      expect(toastr.success)
        .toHaveBeenCalledWith('Proceso ejecutado correctamente.');
    });

    it('should not generate when the dialog is cancelled', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

      component.generateAccountingEntries();

      expect(avalService.generateAccountingEntries).not.toHaveBeenCalled();
    });

    it('should ignore the click while a generation is running', () => {
      component.isGenerating = true;

      component.generateAccountingEntries();

      expect(dialog.open).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAccountingEntries.and.returnValue(
        throwError(() => ({
          error: { errorHeader: { errorMessage: 'Error controlado' } }
        })));

      component.generateAccountingEntries();

      expect(toastr.error).toHaveBeenCalledWith('Error controlado');
    });

    it('should show a default error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAccountingEntries.and.returnValue(
        throwError(() => new Error('boom')));

      component.generateAccountingEntries();

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible generar los asientos contables.');
    });
  });

  describe('#onDownloadXml', () => {
    it('should download the file', () => {
      avalService.downloadXmlFile.and.returnValue(of(new HttpResponse({
        body: new Blob(['<SSC/>']),
        status: 200
      })));

      const anchor = document.createElement('a');
      spyOn(document, 'createElement').and.returnValue(anchor);
      spyOn(anchor, 'click');
      spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
      spyOn(window.URL, 'revokeObjectURL');

      component.onDownloadXml(file);

      expect(avalService.downloadXmlFile).toHaveBeenCalledWith(1);
      expect(anchor.download).toBe('archivo.xml');
    });

    it('should warn when the file is empty', () => {
      avalService.downloadXmlFile.and.returnValue(
        of(new HttpResponse({ body: new Blob([]), status: 200 })));

      component.onDownloadXml(file);

      expect(toastr.warning)
        .toHaveBeenCalledWith('El archivo generado no contiene información.');
    });

    it('should show an error when the download fails', () => {
      avalService.downloadXmlFile.and.returnValue(
        throwError(() => new Error('boom')));

      component.onDownloadXml(file);

      expect(toastr.error)
        .toHaveBeenCalledWith('No fue posible descargar el archivo XML.');
    });
  });
});
