{
  titulo: 'Base Contable',
  url: ['/peru-accounting-report'],
  external: false
},

src/app/views/claims-closing/movements-peru/peru-accounting-report/peru-accounting-report.component.spec.ts

import { ComponentFixture, TestBed } from '@angular/core/testing';
import {
  HttpHeaders,
  HttpResponse
} from '@angular/common/http';
import { of, throwError } from 'rxjs';

import { ToastrService } from 'ngx-toastr';

import { PeruAccountingReportComponent } from './peru-accounting-report.component';
import { PeruAccountingReportService } from '../../services/peru-accounting-report.service';
import { INewGeneralResponse } from '../../models/new-general-response.interface';
import { PeruAccountingReportResponse } from '../../models/peru-accounting-report.model';

describe('PeruAccountingReportComponent', () => {
  let component: PeruAccountingReportComponent;
  let fixture: ComponentFixture<PeruAccountingReportComponent>;
  let service: jasmine.SpyObj<PeruAccountingReportService>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const latestReportResponse:
    INewGeneralResponse<PeruAccountingReportResponse> = {
      correlationId: 'correlation-id',
      responseHeader: {
        returnCode: 200,
        message: 'Success'
      },
      bodyResponse: {
        reportDate: '2026-06-16T10:30:00'
      }
    };

  const generateReportResponse:
    INewGeneralResponse<string> = {
      correlationId: 'correlation-id',
      responseHeader: {
        returnCode: 200,
        message: 'Success'
      },
      bodyResponse:
        'Información del reporte contable generada correctamente.'
    };

  beforeEach(async () => {
    service = jasmine.createSpyObj<PeruAccountingReportService>(
      'PeruAccountingReportService',
      [
        'getLatestReportDate',
        'generateReport',
        'downloadReport'
      ]
    );

    toastr = jasmine.createSpyObj<ToastrService>(
      'ToastrService',
      [
        'success',
        'error',
        'warning'
      ]
    );

    service.getLatestReportDate.and.returnValue(
      of(latestReportResponse)
    );

    await TestBed.configureTestingModule({
      imports: [PeruAccountingReportComponent],
      providers: [
        {
          provide: PeruAccountingReportService,
          useValue: service
        },
        {
          provide: ToastrService,
          useValue: toastr
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(
      PeruAccountingReportComponent
    );

    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should load the latest report date', () => {
      expect(service.getLatestReportDate)
        .toHaveBeenCalled();

      expect(component.reportDate)
        .toBe('2026-06-16T10:30:00');
    });
  });

  describe('#loadLatestReportDate', () => {
    beforeEach(() => {
      service.getLatestReportDate.calls.reset();
    });

    it('should load the latest report date successfully', () => {
      service.getLatestReportDate.and.returnValue(
        of(latestReportResponse)
      );

      component.loadLatestReportDate();

      expect(service.getLatestReportDate)
        .toHaveBeenCalledTimes(1);

      expect(component.reportDate)
        .toBe('2026-06-16T10:30:00');

      expect(component.errorMessage).toBe('');
      expect(component.isLoadingDate).toBeFalse();
    });

    it('should set null when response does not contain a date', () => {
      service.getLatestReportDate.and.returnValue(
        of({
          ...latestReportResponse,
          bodyResponse: {
            reportDate: null
          }
        })
      );

      component.loadLatestReportDate();

      expect(component.reportDate).toBeNull();
      expect(component.isLoadingDate).toBeFalse();
    });

    it('should handle an error while loading the date', () => {
      service.getLatestReportDate.and.returnValue(
        throwError(() => new Error('Network error'))
      );

      component.loadLatestReportDate();

      expect(component.reportDate).toBeNull();

      expect(component.errorMessage).toBe(
        'No fue posible consultar la fecha del último reporte.'
      );

      expect(component.isLoadingDate).toBeFalse();
    });
  });

  describe('#generateReport', () => {
    it('should generate the report successfully', () => {
      service.generateReport.and.returnValue(
        of(generateReportResponse)
      );

      service.getLatestReportDate.calls.reset();

      component.generateReport();

      expect(service.generateReport)
        .toHaveBeenCalledTimes(1);

      expect(toastr.success).toHaveBeenCalledWith(
        generateReportResponse.bodyResponse
      );

      expect(service.getLatestReportDate)
        .toHaveBeenCalledTimes(1);

      expect(component.isGenerating).toBeFalse();
      expect(component.errorMessage).toBe('');
    });

    it('should use the default success message when response is empty', () => {
      service.generateReport.and.returnValue(
        of({
          ...generateReportResponse,
          bodyResponse: ''
        })
      );

      component.generateReport();

      expect(toastr.success).toHaveBeenCalledWith(
        'Información generada correctamente.'
      );
    });

    it('should not make a duplicated request while generating', () => {
      component.isGenerating = true;

      component.generateReport();

      expect(service.generateReport)
        .not.toHaveBeenCalled();
    });

    it('should handle an error while generating the report', () => {
      service.generateReport.and.returnValue(
        throwError(() => new Error('Generation error'))
      );

      component.generateReport();

      expect(component.errorMessage).toBe(
        'No fue posible generar la información del reporte.'
      );

      expect(toastr.error).toHaveBeenCalledWith(
        component.errorMessage
      );

      expect(component.isGenerating).toBeFalse();
    });
  });

  describe('#downloadReport', () => {
    let createObjectUrlSpy: jasmine.Spy;
    let revokeObjectUrlSpy: jasmine.Spy;
    let anchor: HTMLAnchorElement;

    beforeEach(() => {
      anchor = document.createElement('a');

      spyOn(anchor, 'click');

      spyOn(document, 'createElement')
        .and.returnValue(anchor);

      createObjectUrlSpy = spyOn(
        window.URL,
        'createObjectURL'
      ).and.returnValue('blob:report');

      revokeObjectUrlSpy = spyOn(
        window.URL,
        'revokeObjectURL'
      );
    });

    it('should download the Excel report successfully', () => {
      const file = new Blob(
        ['excel-content'],
        {
          type:
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
      );

      const response = new HttpResponse<Blob>({
        body: file,
        status: 200,
        headers: new HttpHeaders({
          'Content-Disposition':
            'attachment; filename="ReporteContablePeru.xlsx"'
        })
      });

      service.downloadReport.and.returnValue(
        of(response)
      );

      component.downloadReport();

      expect(service.downloadReport)
        .toHaveBeenCalledTimes(1);

      expect(createObjectUrlSpy)
        .toHaveBeenCalledWith(file);

      expect(anchor.href).toContain('blob:report');

      expect(anchor.download)
        .toBe('ReporteContablePeru.xlsx');

      expect(anchor.click)
        .toHaveBeenCalled();

      expect(revokeObjectUrlSpy)
        .toHaveBeenCalledWith('blob:report');

      expect(toastr.success).toHaveBeenCalledWith(
        'Reporte descargado correctamente.'
      );

      expect(component.isDownloading).toBeFalse();
    });

    it('should use the default filename when header is missing', () => {
      const file = new Blob(['excel-content']);

      service.downloadReport.and.returnValue(
        of(
          new HttpResponse<Blob>({
            body: file,
            status: 200
          })
        )
      );

      component.downloadReport();

      expect(anchor.download)
        .toBe('ReporteContablePeru.xlsx');
    });

    it('should display a warning when the file is empty', () => {
      const emptyFile = new Blob([]);

      service.downloadReport.and.returnValue(
        of(
          new HttpResponse<Blob>({
            body: emptyFile,
            status: 200
          })
        )
      );

      component.downloadReport();

      expect(toastr.warning).toHaveBeenCalledWith(
        'El archivo generado no contiene información.'
      );

      expect(anchor.click)
        .not.toHaveBeenCalled();

      expect(createObjectUrlSpy)
        .not.toHaveBeenCalled();

      expect(component.isDownloading).toBeFalse();
    });

    it('should not make a duplicated request while downloading', () => {
      component.isDownloading = true;

      component.downloadReport();

      expect(service.downloadReport)
        .not.toHaveBeenCalled();
    });

    it('should handle an error while downloading the report', () => {
      service.downloadReport.and.returnValue(
        throwError(() => new Error('Download error'))
      );

      component.downloadReport();

      expect(component.errorMessage).toBe(
        'No fue posible descargar el reporte contable.'
      );

      expect(toastr.error).toHaveBeenCalledWith(
        component.errorMessage
      );

      expect(component.isDownloading).toBeFalse();
    });
  });
});
