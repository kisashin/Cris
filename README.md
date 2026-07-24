import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of } from 'rxjs';
import { ToastrService } from 'ngx-toastr';

import { ReportDataComponent } from './report-data-ca.component';
import { ReportDataService } from '../../services/report-data.service';

describe('ReportDataComponent', () => {

  let component: ReportDataComponent;
  let fixture: ComponentFixture<ReportDataComponent>;

  const reportDataServiceMock = {
    getReportStatus: jasmine
      .createSpy()
      .and.returnValue(of([])),

    getInconsistentCoverages: jasmine
      .createSpy()
      .and.returnValue(of([])),

    generateInformation: jasmine
      .createSpy()
      .and.returnValue(of(void 0)),

    downloadDataReport: jasmine
      .createSpy(),

    downloadMovementsReport: jasmine
      .createSpy(),

    downloadFile: jasmine
      .createSpy()
  };

  const toastrServiceMock = {
    success: jasmine.createSpy(),
    error: jasmine.createSpy(),
    warning: jasmine.createSpy()
  };

  beforeEach(async () => {

    await TestBed.configureTestingModule({
      declarations: [
        ReportDataComponent
      ],
      imports: [
        NoopAnimationsModule
      ],
      providers: [
        {
          provide: ReportDataService,
          useValue: reportDataServiceMock
        },
        {
          provide: ToastrService,
          useValue: toastrServiceMock
        }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(
      ReportDataComponent
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

});
