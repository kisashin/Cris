import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';

import { AccountingEntryComponent } from './accounting-entry.component';
import { AccountingEntryService } from '../services/accounting-entry.service';
import { AutenticacionService } from '../../../login/service/autenticacion.service';

describe('AccountingEntryComponent', () => {

  let component: AccountingEntryComponent;
  let fixture: ComponentFixture<AccountingEntryComponent>;
  let accountingEntryService: jasmine.SpyObj<AccountingEntryService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let toastr: jasmine.SpyObj<ToastrService>;
  let autenticacionService: any;

  const csvFile = new File(['contenido'], '326CO21SR0122026090110.csv', {
    type: 'text/csv'
  });

  const generatedFile = {
    id: 1,
    product: '2005',
    journalType: 'SINIE',
    fileName: '2005_202606SINIE_20052026006.XML',
    generationDate: '02/09/2026 03:04:45'
  };

  const openDialog = (confirmed: boolean) => {
    dialog.open.and.returnValue({
      afterClosed: () => of(confirmed)
    } as any);
  };

  beforeEach(async () => {

    accountingEntryService = jasmine.createSpyObj(
      'AccountingEntryService',
      [
        'getAccountingDate',
        'getProducts',
        'getFiles',
        'loadClaims',
        'previewAccountingEntry',
        'registerAccountingEntry',
        'getAccountSummary',
        'sendAccountingEntry',
        'downloadFile'
      ]
    );

    dialog = jasmine.createSpyObj('MatDialog', ['open']);

    toastr = jasmine.createSpyObj(
      'ToastrService',
      ['success', 'error', 'warning']
    );

    autenticacionService = {
      getUserAuthenticate: { user: 'j36147' }
    };

    accountingEntryService.getAccountingDate.and.returnValue(
      of({ bodyResponse: { accountingDate: '20260630' } })
    );

    accountingEntryService.getProducts.and.returnValue(
      of({ bodyResponse: [{ product: '2005' }] })
    );

    accountingEntryService.getFiles.and.returnValue(
      of({ bodyResponse: [] })
    );

    await TestBed.configureTestingModule({

      declarations: [AccountingEntryComponent],

      providers: [
        { provide: AccountingEntryService, useValue: accountingEntryService },
        { provide: MatDialog, useValue: dialog },
        { provide: ToastrService, useValue: toastr },
        { provide: AutenticacionService, useValue: autenticacionService }
      ],

      schemas: [NO_ERRORS_SCHEMA]

    }).compileComponents();

    fixture = TestBed.createComponent(AccountingEntryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load accounting date', () => {
    expect(component.accountingDate).toBe('20260630');
  });

  it('should load products', () => {
    expect(component.products.length).toBe(1);
  });

  it('should build comment automatically', () => {
    expect(component.comment).toBe('2005_202606');
  });

  it('should load generated files on init', () => {
    expect(accountingEntryService.getFiles).toHaveBeenCalled();
    expect(component.files.length).toBe(0);
  });

  it('should leave the file list empty when the query fails', () => {
    accountingEntryService.getFiles.and.returnValue(throwError(() => new Error()));

    component.loadFiles();

    expect(component.files.length).toBe(0);
  });

  it('should clear the state when the product changes', () => {
    component.dataSource = [{ journalType: 'SINIE' }];
    component.sendMessage = 'mensaje';
    component.message = 'mensaje';
    component.selectedFile = csvFile;

    component.onProductChange();

    expect(component.dataSource.length).toBe(0);
    expect(component.sendMessage).toBe('');
    expect(component.message).toBe('');
    expect(component.selectedFile).toBeNull();
  });

  it('should keep the selected file', () => {
    const event = { target: { files: [csvFile] } } as unknown as Event;

    component.onFileSelected(event);

    expect(component.selectedFile?.name).toBe('326CO21SR0122026090110.csv');
  });

  it('should clear the selection when no file is chosen', () => {
    const event = { target: { files: [] } } as unknown as Event;

    component.onFileSelected(event);

    expect(component.selectedFile).toBeNull();
  });

  it('should warn when loading without a file', () => {
    component.loadClaims();

    expect(toastr.warning).toHaveBeenCalled();
    expect(accountingEntryService.loadClaims).not.toHaveBeenCalled();
  });

  it('should warn when loading without a product', () => {
    component.selectedProduct = '';
    component.selectedFile = csvFile;

    component.loadClaims();

    expect(toastr.warning).toHaveBeenCalled();
    expect(accountingEntryService.loadClaims).not.toHaveBeenCalled();
  });

  it('should load the file and show the message', () => {
    accountingEntryService.loadClaims.and.returnValue(
      of({
        bodyResponse: {
          message: '5 Registros Cargados',
          totalRows: 5,
          incompleteRows: 0
        }
      })
    );

    component.selectedFile = csvFile;

    component.loadClaims();

    expect(component.message).toBe('5 Registros Cargados');
    expect(component.loading).toBeFalse();
    expect(accountingEntryService.loadClaims)
      .toHaveBeenCalledWith(csvFile, '2005', 'j36147');
  });

  it('should warn about incomplete rows', () => {
    accountingEntryService.loadClaims.and.returnValue(
      of({
        bodyResponse: {
          message: '5 Registros Cargados',
          totalRows: 5,
          incompleteRows: 2
        }
      })
    );

    component.selectedFile = csvFile;

    component.loadClaims();

    expect(toastr.warning).toHaveBeenCalled();
  });

  it('should show an error when the load fails', () => {
    accountingEntryService.loadClaims.and.returnValue(
      throwError(() => ({
        error: { errorDetail: { message: 'El archivo es requerido.' } }
      }))
    );

    component.selectedFile = csvFile;

    component.loadClaims();

    expect(toastr.error).toHaveBeenCalledWith('El archivo es requerido.');
    expect(component.loading).toBeFalse();
  });

  it('should use the fallback message when the error has no detail', () => {
    accountingEntryService.loadClaims.and.returnValue(
      throwError(() => new Error())
    );

    component.selectedFile = csvFile;

    component.loadClaims();

    expect(toastr.error)
      .toHaveBeenCalledWith('No fue posible cargar el archivo.');
  });

  it('should generate the entry with the preview columns', () => {
    accountingEntryService.previewAccountingEntry.and.returnValue(
      of({ bodyResponse: [{ journalType: 'SINIE', transactionAmount: 1500.567 }] })
    );

    component.generateAccountingEntry();

    expect(component.displayedColumns).toBe(component.generateColumns);
    expect(component.dataSource[0].transactionAmount).toBe(1500.57);
  });

  it('should show an error when the entry generation fails', () => {
    accountingEntryService.previewAccountingEntry.and.returnValue(
      throwError(() => new Error())
    );

    component.generateAccountingEntry();

    expect(toastr.error).toHaveBeenCalled();
    expect(component.loading).toBeFalse();
  });

  it('should register the entry with a fixed message', () => {
    accountingEntryService.registerAccountingEntry.and.returnValue(
      of({ bodyResponse: null })
    );

    component.registerAccountingEntry();

    expect(component.sendMessage).toBe('Asiento registrado');
  });

  it('should show an error when the registration fails', () => {
    accountingEntryService.registerAccountingEntry.and.returnValue(
      throwError(() => new Error())
    );

    component.registerAccountingEntry();

    expect(toastr.error).toHaveBeenCalled();
  });

  it('should query the account summary with the total columns', () => {
    accountingEntryService.getAccountSummary.and.returnValue(
      of({ bodyResponse: [{ product: '2005', debit: 100 }] })
    );

    component.getAccountSummary();

    expect(component.displayedColumns).toBe(component.totalColumns);
    expect(component.dataSource.length).toBe(1);
  });

  it('should show an error when the summary fails', () => {
    accountingEntryService.getAccountSummary.and.returnValue(
      throwError(() => new Error())
    );

    component.getAccountSummary();

    expect(toastr.error).toHaveBeenCalled();
  });

  it('should not generate the XML when the dialog is cancelled', () => {
    openDialog(false);

    component.sendAccountingEntry();

    expect(accountingEntryService.sendAccountingEntry).not.toHaveBeenCalled();
  });

  it('should generate the XML and refresh the file list when confirmed', () => {
    openDialog(true);

    accountingEntryService.sendAccountingEntry.and.returnValue(
      of({ bodyResponse: { message: 'Interfaz generada correctamente.' } })
    );

    accountingEntryService.getFiles.and.returnValue(
      of({ bodyResponse: [generatedFile] })
    );

    component.sendAccountingEntry();

    expect(component.sendMessage).toBe('Interfaz generada correctamente.');
    expect(component.files.length).toBe(1);
    expect(accountingEntryService.sendAccountingEntry).toHaveBeenCalledWith({
      product: '2005',
      comment: '2005_202606',
      user: 'j36147'
    });
  });

  it('should show an error when the XML generation fails', () => {
    openDialog(true);

    accountingEntryService.sendAccountingEntry.and.returnValue(
      throwError(() => new Error())
    );

    component.sendAccountingEntry();

    expect(toastr.error).toHaveBeenCalled();
    expect(component.loading).toBeFalse();
  });

  it('should ignore the generation while another one is running', () => {
    component.loading = true;

    component.sendAccountingEntry();

    expect(dialog.open).not.toHaveBeenCalled();
  });

  it('should download the XML file', () => {
    const blob = new Blob(['<SSC/>'], { type: 'application/xml' });

    accountingEntryService.downloadFile.and.returnValue(
      of(new HttpResponse({ body: blob }))
    );

    spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
    spyOn(window.URL, 'revokeObjectURL');

    component.onDownloadXml(generatedFile);

    expect(window.URL.createObjectURL).toHaveBeenCalled();
    expect(window.URL.revokeObjectURL).toHaveBeenCalled();
  });

  it('should warn when the downloaded file is empty', () => {
    accountingEntryService.downloadFile.and.returnValue(
      of(new HttpResponse({ body: new Blob([]) }))
    );

    component.onDownloadXml(generatedFile);

    expect(toastr.warning).toHaveBeenCalled();
  });

  it('should show an error when the download fails', () => {
    accountingEntryService.downloadFile.and.returnValue(
      throwError(() => new Error())
    );

    component.onDownloadXml(generatedFile);

    expect(toastr.error).toHaveBeenCalled();
  });

  it('should send an empty user when there is no session', () => {
    autenticacionService.getUserAuthenticate = null;

    accountingEntryService.loadClaims.and.returnValue(
      of({ bodyResponse: { message: 'ok', totalRows: 1, incompleteRows: 0 } })
    );

    component.selectedFile = csvFile;

    component.loadClaims();

    expect(accountingEntryService.loadClaims)
      .toHaveBeenCalledWith(csvFile, '2005', '');
  });

});
