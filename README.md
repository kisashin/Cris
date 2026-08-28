import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { ClaimsClosingCardifComponent } from './claims-closing-cardif.component';
import { ClosingCardifService } from '../../services/closing-cardif.service';
import { IColombiaXmlFile } from '../../models/colombia-accounting-result.model';

describe('ClaimsClosingCardifComponent', () => {
  let component: ClaimsClosingCardifComponent;
  let fixture: ComponentFixture<ClaimsClosingCardifComponent>;
  let cardifService: jasmine.SpyObj<ClosingCardifService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const file: IColombiaXmlFile = {
    id: 1,
    period: '202608',
    family: 'ReasegCardif',
    movementType: 'Pago',
    fileName: 'archivo.xml',
    lineCount: 4,
    processDate: '28/08/2026 10:00:00 a. m.',
    status: 'GENERADO'
  };

  const blobResponse = (size = 10): HttpResponse<Blob> =>
    new HttpResponse({
      body: new Blob(['x'.repeat(size)], { type: 'application/xml' }),
      status: 200
    });

  beforeEach(async () => {
    cardifService = jasmine.createSpyObj('ClosingCardifService', [
      'findGeneratedFiles',
      'generateAccountingEntries',
      'downloadXmlFile'
    ]);
    dialog = jasmine.createSpyObj('MatDialog', ['open']);
    toastr = jasmine.createSpyObj('ToastrService', [
      'success', 'error', 'warning'
    ]);

    cardifService.findGeneratedFiles.and.returnValue(
      of({ bodyResponse: [file] } as any));

    await TestBed.configureTestingModule({
      imports: [ClaimsClosingCardifComponent, NoopAnimationsModule],
      providers: [
        { provide: ClosingCardifService, useValue: cardifService },
        { provide: MatDialog, useValue: dialog },
        { provide: ToastrService, useValue: toastr }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ClaimsClosingCardifComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#loadGeneratedFiles', () => {
    it('should load the generated files on init', () => {
      expect(component.dataSource.length).toBe(1);
      expect(component.dataSource[0].family).toBe('ReasegCardif');
      expect(component.isLoading).toBeFalse();
    });

    it('should use an empty list when the body is null', () => {
      cardifService.findGeneratedFiles.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
    });

    it('should clear the list when the request fails', () => {
      cardifService.findGeneratedFiles.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadGeneratedFiles();

      expect(component.dataSource).toEqual([]);
      expect(component.isLoading).toBeFalse();
    });
  });

  describe('#generateAccountingEntries', () => {
    it('should generate when the dialog is confirmed', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      cardifService.generateAccountingEntries.and.returnValue(of({
        bodyResponse: { message: 'Asientos generados con éxito.' }
      } as any));

      component.generateAccountingEntries();

      expect(cardifService.generateAccountingEntries).toHaveBeenCalled();
      expect(toastr.success)
        .toHaveBeenCalledWith('Asientos generados con éxito.');
      expect(component.isGenerating).toBeFalse();
    });

    it('should show a default message when the body has none', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      cardifService.generateAccountingEntries.and.returnValue(
        of({ bodyResponse: null } as any));

      component.generateAccountingEntries();

      expect(toastr.success)
        .toHaveBeenCalledWith('Proceso ejecutado correctamente.');
    });

    it('should not generate when the dialog is cancelled', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

      component.generateAccountingEntries();

      expect(cardifService.generateAccountingEntries).not.toHaveBeenCalled();
    });

    it('should ignore the click while a generation is running', () => {
      component.isGenerating = true;

      component.generateAccountingEntries();

      expect(dialog.open).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      cardifService.generateAccountingEntries.and.returnValue(
        throwError(() => ({
          error: { errorHeader: { errorMessage: 'Error controlado' } }
        })));

      component.generateAccountingEntries();

      expect(toastr.error).toHaveBeenCalledWith('Error controlado');
      expect(component.isGenerating).toBeFalse();
    });

    it('should show a default error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      cardifService.generateAccountingEntries.and.returnValue(
        throwError(() => new Error('boom')));

      component.generateAccountingEntries();

      expect(toastr.error)
        .toHaveBeenCalledWith('No fue posible generar los asientos contables.');
    });
  });

  describe('#onDownloadXml', () => {
    it('should download the file', () => {
      cardifService.downloadXmlFile.and.returnValue(of(blobResponse()));
      const anchor = document.createElement('a');
      spyOn(document, 'createElement').and.returnValue(anchor);
      spyOn(anchor, 'click');
      spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
      spyOn(window.URL, 'revokeObjectURL');

      component.onDownloadXml(file);

      expect(cardifService.downloadXmlFile).toHaveBeenCalledWith(1);
      expect(anchor.download).toBe('archivo.xml');
      expect(anchor.click).toHaveBeenCalled();
      expect(window.URL.revokeObjectURL).toHaveBeenCalled();
    });

    it('should warn when the file is empty', () => {
      cardifService.downloadXmlFile.and.returnValue(
        of(new HttpResponse({ body: new Blob([]), status: 200 })));

      component.onDownloadXml(file);

      expect(toastr.warning)
        .toHaveBeenCalledWith('El archivo generado no contiene información.');
    });

    it('should warn when the body is null', () => {
      cardifService.downloadXmlFile.and.returnValue(
        of(new HttpResponse<Blob>({ body: null, status: 200 })));

      component.onDownloadXml(file);

      expect(toastr.warning).toHaveBeenCalled();
    });

    it('should show an error when the download fails', () => {
      cardifService.downloadXmlFile.and.returnValue(
        throwError(() => new Error('boom')));

      component.onDownloadXml(file);

      expect(toastr.error)
        .toHaveBeenCalledWith('No fue posible descargar el archivo XML.');
    });
  });
});
