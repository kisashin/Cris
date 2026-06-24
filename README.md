src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.spec.ts



src/app/views/claims-closing/services/cardif-peru-closing.service.ts
src/app/views/claims-closing/services/cardif-peru-closing.service.spec.ts

import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { INewGeneralResponse } from '../models/new-general-response.interface';

import { ComponentFixture, TestBed } from '@angular/core/testing';
import {
  HttpHeaders,
  HttpResponse
} from '@angular/common/http';
import { of, throwError } from 'rxjs';

import { ToastrService } from 'ngx-toastr';

import { CardifPeruClosingComponent } from './cardif-peru-closing.component';
import { CardifPeruClosingService } from '../../services/cardif-peru-closing.service';
import { INewGeneralResponse } from '../../models/new-general-response.interface';

describe('CardifPeruClosingComponent', () => {
  let component: CardifPeruClosingComponent;
  let fixture: ComponentFixture<CardifPeruClosingComponent>;
  let service: jasmine.SpyObj<CardifPeruClosingService>;
  let toastr: jasmine.SpyObj<ToastrService>;

  const generateResponse: INewGeneralResponse<string> = {
    correlationId: 'correlation-id',
    responseHeader: {
      returnCode: 200,
      message: 'Success'
    },
    bodyResponse: 'Asientos generados con éxito.'
  };

  beforeEach(async () => {
    service = jasmine.createSpyObj<CardifPeruClosingService>(
      'CardifPeruClosingService',
      [
        'generateAccountingEntries',
        'downloadMovementsReport'
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

    await TestBed.configureTestingModule({
      imports: [CardifPeruClosingComponent],
      providers: [
        {
          provide: CardifPeruClosingService,
          useValue: service
        },
        {
          provide: ToastrService,
          useValue: toastr
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(CardifPeruClosingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#generateAccountingEntries', () => {
    it('should generate accounting entries successfully', () => {
      service.generateAccountingEntries.and.returnValue(
        of(generateResponse)
      );

      component.generateAccountingEntries();

      expect(service.generateAccountingEntries)
        .toHaveBeenCalledTimes(1);

      expect(toastr.success).toHaveBeenCalledWith(
        generateResponse.bodyResponse
      );

      expect(component.isGenerating).toBeFalse();
      expect(component.errorMessage).toBe('');
    });

    it('should use the default message when response is empty', () => {
      service.generateAccountingEntries.and.returnValue(
        of({
          ...generateResponse,
          bodyResponse: ''
        })
      );

      component.generateAccountingEntries();

      expect(toastr.success).toHaveBeenCalledWith(
        'Proceso ejecutado correctamente.'
      );
    });

    it('should not make a duplicated request while generating', () => {
      component.isGenerating = true;

      component.generateAccountingEntries();

      expect(service.generateAccountingEntries)
        .not.toHaveBeenCalled();
    });

    it('should handle an error while generating', () => {
      service.generateAccountingEntries.and.returnValue(
        throwError(() => new Error('Generation error'))
      );

      component.generateAccountingEntries();

      expect(component.errorMessage).toBe(
        'No fue posible generar los asientos contables.'
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
      spyOn(document, 'createElement').and.returnValue(anchor);

      createObjectUrlSpy = spyOn(
        window.URL,
        'createObjectURL'
      ).and.returnValue('blob:report');

      revokeObjectUrlSpy = spyOn(window.URL, 'revokeObjectURL');
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
            'attachment; filename="ReporteMovimientosCardifPeru.xlsx"'
        })
      });

      service.downloadMovementsReport.and.returnValue(of(response));

      component.downloadReport();

      expect(service.downloadMovementsReport)
        .toHaveBeenCalledTimes(1);

      expect(createObjectUrlSpy).toHaveBeenCalledWith(file);
      expect(anchor.href).toContain('blob:report');
      expect(anchor.download).toBe('ReporteMovimientosCardifPeru.xlsx');
      expect(anchor.click).toHaveBeenCalled();
      expect(revokeObjectUrlSpy).toHaveBeenCalledWith('blob:report');

      expect(toastr.success).toHaveBeenCalledWith(
        'Reporte descargado correctamente.'
      );

      expect(component.isDownloading).toBeFalse();
    });

    it('should use the default filename when header is missing', () => {
      const file = new Blob(['excel-content']);

      service.downloadMovementsReport.and.returnValue(
        of(
          new HttpResponse<Blob>({
            body: file,
            status: 200
          })
        )
      );

      component.downloadReport();

      expect(anchor.download).toBe('ReporteMovimientosCardifPeru.xlsx');
    });

    it('should display a warning when the file is empty', () => {
      const emptyFile = new Blob([]);

      service.downloadMovementsReport.and.returnValue(
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

      expect(anchor.click).not.toHaveBeenCalled();
      expect(createObjectUrlSpy).not.toHaveBeenCalled();
      expect(component.isDownloading).toBeFalse();
    });

    it('should not make a duplicated request while downloading', () => {
      component.isDownloading = true;

      component.downloadReport();

      expect(service.downloadMovementsReport)
        .not.toHaveBeenCalled();
    });

    it('should handle an error while downloading', () => {
      service.downloadMovementsReport.and.returnValue(
        throwError(() => new Error('Download error'))
      );

      component.downloadReport();

      expect(component.errorMessage).toBe(
        'No fue posible descargar el reporte de movimientos.'
      );

      expect(toastr.error).toHaveBeenCalledWith(
        component.errorMessage
      );

      expect(component.isDownloading).toBeFalse();
    });
  });
});
