import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { IMetaColumn } from '../../models/IMetaColumn.models';
import {
  ClaimMovement,
  IndividualNews,
  IndividualNewsRequest
} from '../../models/IndividualNews.model';
import { IndividualNewsService } from '../../services/individual-news.service';
import { ProfileService } from '@core/services/perfiles/perfiles.service';

@Component({
  selector: 'app-individual-news',
  templateUrl: './individual-news.component.html',
  styleUrl: './individual-news.component.scss',
  standalone: false
})
export class IndividualNewsComponent implements OnInit {

  private readonly menuKey = 'ClaimsClosing';

  public searchForm!: FormGroup;
  public updateForm!: FormGroup;
  public deleteForm!: FormGroup;

  public showUpdateForm = false;
  public showDeleteForm = false;
  public showMovements = false;

  public canRequest = false;
  public canApprove = false;

  public movements: ClaimMovement[] = [];
  public pendingNews: IndividualNews[] = [];
  public selectedNews: IndividualNews | null = null;

  public movementColumns: IMetaColumn[] = [];
  public newsColumns: IMetaColumn[] = [];

  constructor(
    private fb: FormBuilder,
    private individualNewsSrv: IndividualNewsService,
    private profileService: ProfileService,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.canRequest = this.profileService.hasPermission('solicitarNovedad', this.menuKey);
    this.canApprove = this.profileService.hasPermission('aprobarNovedad', this.menuKey);

    this.buildForms();
    this.buildColumns();
    this.loadPendingNews();
  }

  private buildForms(): void {
    this.searchForm = this.fb.group({
      claimNumber: ['', Validators.required]
    });

    this.updateForm = this.fb.group({
      idCarvajal: [null, Validators.required],
      movementType: ['', [Validators.required, Validators.maxLength(100)]],
      partner: ['', [Validators.required, Validators.maxLength(255)]],
      coverage: ['', [Validators.required, Validators.maxLength(255)]],
      cardifId: ['', [Validators.required, Validators.maxLength(255)]],
      claimKey: ['', [Validators.required, Validators.maxLength(255)]],
      branchCode: ['', [Validators.required, Validators.maxLength(120)]],
      claimNumber: ['', [Validators.required, Validators.maxLength(255)]],
      partnerCode: [null, Validators.required],
      claimStatus: ['', [Validators.required, Validators.maxLength(100)]],
      majorStatus: ['', [Validators.required, Validators.maxLength(255)]],
      channel: ['', [Validators.required, Validators.maxLength(255)]],
      pandemic: ['', [Validators.required, Validators.maxLength(255)]],
      justification: ['', [Validators.required, Validators.maxLength(255)]],
      paymentBeneficiary: ['', Validators.maxLength(255)],
      coinsuranceType: [null],
      retainedCoinsuranceValue: [null],
      cededCoinsuranceValue: [null],
      birthDate: [null],
      occurrenceDate: [null],
      partnerNoticeDate: [null],
      cardifNoticeDate: [null]
    });

    this.deleteForm = this.fb.group({
      idCarvajal: [null, Validators.required],
      movementType: [{ value: '', disabled: true }],
      partner: [{ value: '', disabled: true }],
      coverage: [{ value: '', disabled: true }],
      branchCode: [{ value: '', disabled: true }],
      claimNumber: [{ value: '', disabled: true }],
      justification: ['', [Validators.required, Validators.maxLength(255)]]
    });
  }

  private buildColumns(): void {
    this.movementColumns = [
      { title: 'Nro Siniestro', field: 'claimNumber' },
      { title: 'Nro Identificacion', field: 'identificationNumber' },
      { title: 'Producto', field: 'productCode' },
      { title: 'Cod Plan', field: 'planCode' },
      { title: 'Cobertura', field: 'coverage' },
      { title: 'Ramo', field: 'branchCode' },
      { title: 'Valor', field: 'movementValue' },
      { title: 'Fecha Movimiento', field: 'movementDate' },
      { title: 'Tipo Movimiento', field: 'movementType' }
    ];

    if (this.canRequest) {
      this.movementColumns.push({
        title: 'Acciones', field: 'actions', actions: [
          {
            action: (row: ClaimMovement) => this.openUpdateForm(row),
            fasIcon: 'fal fa-edit',
            tooltip: () => 'Editar',
            isMenu: false,
            actionEditDeleteCircle: true,
            edit: true
          },
          {
            action: (row: ClaimMovement) => this.openDeleteForm(row),
            fasIcon: 'fal fa-times-circle pointer',
            tooltip: () => 'Eliminar',
            isMenu: false,
            actionEditDeleteCircle: true,
            delete: true
          }
        ]
      });
    }

    this.newsColumns = [
      { title: 'Codigo', field: 'code' },
      { title: 'ID Carvajal', field: 'idCarvajal' },
      { title: 'Nro Siniestro', field: 'claimNumber' },
      { title: 'Tipo Novedad', field: 'newsType' },
      { title: 'Fecha Proceso', field: 'processDate' },
      { title: 'Solicitante', field: 'requestUser' },
      { title: 'Justificacion', field: 'justification' }
    ];

    const newsActions: any[] = [
      {
        action: (row: IndividualNews) => this.viewNews(row),
        fasIcon: 'fal fa-eye',
        tooltip: () => 'Ver',
        isMenu: false,
        actionEditDeleteCircle: true,
        edit: true
      }
    ];

    if (this.canApprove) {
      newsActions.push(
        {
          action: (row: IndividualNews) => this.approve(row),
          fasIcon: 'fal fa-check-circle',
          tooltip: () => 'Aprobar',
          isMenu: false,
          actionEditDeleteCircle: true,
          edit: true
        },
        {
          action: (row: IndividualNews) => this.cancel(row),
          fasIcon: 'fal fa-times-circle pointer',
          tooltip: () => 'Cancelar',
          isMenu: false,
          actionEditDeleteCircle: true,
          delete: true
        }
      );
    }

    this.newsColumns.push({ title: 'Acciones', field: 'actions', actions: newsActions });
  }

  onSearch(): void {
    if (this.searchForm.invalid) {
      return;
    }

    this.resetForms();
    const claimNumber = this.searchForm.value.claimNumber;

    this.individualNewsSrv.buscarMovimientos(claimNumber).subscribe({
      next: (response) => {
        this.movements = response?.bodyResponse ?? [];
        this.showMovements = true;
        if (this.movements.length === 0) {
          this.toastr.info('No se encontraron registros para esta consulta');
        }
      },
      error: (error) => this.handleError(error, 'Error al consultar los movimientos')
    });
  }

  openUpdateForm(row: ClaimMovement): void {
    this.showUpdateForm = true;
    this.showDeleteForm = false;
    this.selectedNews = null;

    this.updateForm.patchValue({
      idCarvajal: row.idCarvajal,
      movementType: row.movementType,
      partner: row.partner,
      coverage: row.coverage,
      cardifId: row.cardifId,
      claimKey: row.claimKey,
      branchCode: row.branchCode,
      claimNumber: row.claimNumber,
      partnerCode: row.partnerCode,
      claimStatus: row.claimStatus,
      majorStatus: row.majorStatus,
      channel: row.channel,
      pandemic: row.pandemic,
      justification: '',
      paymentBeneficiary: row.paymentBeneficiary,
      coinsuranceType: row.coinsuranceType,
      retainedCoinsuranceValue: row.retainedCoinsuranceValue,
      cededCoinsuranceValue: row.cededCoinsuranceValue,
      birthDate: row.birthDate,
      occurrenceDate: row.occurrenceDate,
      partnerNoticeDate: row.partnerNoticeDate,
      cardifNoticeDate: row.cardifNoticeDate
    });
  }

  openDeleteForm(row: ClaimMovement): void {
    this.showDeleteForm = true;
    this.showUpdateForm = false;
    this.selectedNews = null;

    this.deleteForm.patchValue({
      idCarvajal: row.idCarvajal,
      movementType: row.movementType,
      partner: row.partner,
      coverage: row.coverage,
      branchCode: row.branchCode,
      claimNumber: row.claimNumber,
      justification: ''
    });
  }

  onSaveUpdate(): void {
    if (this.updateForm.invalid) {
      this.updateForm.markAllAsTouched();
      return;
    }

    const value = this.updateForm.value;

    const payload: IndividualNewsRequest = {
      idCarvajal: value.idCarvajal,
      movementType: value.movementType,
      partner: value.partner,
      coverage: value.coverage,
      cardifId: value.cardifId,
      claimKey: value.claimKey,
      branchCode: value.branchCode,
      claimNumber: value.claimNumber,
      partnerCode: Number(value.partnerCode),
      claimStatus: value.claimStatus,
      majorStatus: value.majorStatus,
      channel: value.channel,
      pandemic: value.pandemic,
      justification: value.justification,
      paymentBeneficiary: value.paymentBeneficiary || null,
      coinsuranceType: this.toNumber(value.coinsuranceType),
      retainedCoinsuranceValue: this.toNumber(value.retainedCoinsuranceValue),
      cededCoinsuranceValue: this.toNumber(value.cededCoinsuranceValue),
      birthDate: this.toIsoDateTime(value.birthDate),
      occurrenceDate: this.toIsoDateTime(value.occurrenceDate),
      partnerNoticeDate: this.toIsoDateTime(value.partnerNoticeDate),
      cardifNoticeDate: this.toIsoDateTime(value.cardifNoticeDate)
    };

    this.individualNewsSrv.solicitarActualizacion(payload).subscribe({
      next: () => {
        this.toastr.success('Registro procesado para autorizar');
        this.afterRequest();
      },
      error: (error) => this.handleError(error, 'Error al registrar la novedad')
    });
  }

  onSaveDelete(): void {
    if (this.deleteForm.invalid) {
      this.deleteForm.markAllAsTouched();
      return;
    }

    const value = this.deleteForm.getRawValue();

    this.individualNewsSrv.solicitarEliminacion({
      idCarvajal: value.idCarvajal,
      justification: value.justification
    }).subscribe({
      next: () => {
        this.toastr.success('Registro procesado para autorizar');
        this.afterRequest();
      },
      error: (error) => this.handleError(error, 'Error al registrar la novedad')
    });
  }

  viewNews(row: IndividualNews): void {
    this.individualNewsSrv.consultarNovedad(row.code).subscribe({
      next: (response) => {
        this.selectedNews = response?.bodyResponse ?? null;
        this.showUpdateForm = false;
        this.showDeleteForm = false;
      },
      error: (error) => this.handleError(error, 'Error al consultar la novedad')
    });
  }

  approve(row: IndividualNews): void {
    this.individualNewsSrv.aprobar(row.code).subscribe({
      next: () => {
        this.toastr.success('Novedad aplicada con exito');
        this.afterResolution();
      },
      error: (error) => this.handleError(error, 'Error al aprobar la novedad')
    });
  }

  cancel(row: IndividualNews): void {
    this.individualNewsSrv.cancelar(row.code).subscribe({
      next: () => {
        this.toastr.success('Novedad cancelada con exito');
        this.afterResolution();
      },
      error: (error) => this.handleError(error, 'Error al cancelar la novedad')
    });
  }

  loadPendingNews(): void {
    this.individualNewsSrv.consultarPendientes().subscribe({
      next: (response) => {
        this.pendingNews = response?.bodyResponse ?? [];
      },
      error: (error) => this.handleError(error, 'Error al consultar las novedades pendientes')
    });
  }

  private afterRequest(): void {
    this.resetForms();
    this.loadPendingNews();
    if (this.searchForm.valid) {
      this.onSearchSilent();
    }
  }

  private afterResolution(): void {
    this.selectedNews = null;
    this.loadPendingNews();
    if (this.searchForm.valid) {
      this.onSearchSilent();
    }
  }

  private onSearchSilent(): void {
    this.individualNewsSrv.buscarMovimientos(this.searchForm.value.claimNumber).subscribe({
      next: (response) => {
        this.movements = response?.bodyResponse ?? [];
      },
      error: () => {
        this.movements = [];
      }
    });
  }

  private resetForms(): void {
    this.showUpdateForm = false;
    this.showDeleteForm = false;
    this.selectedNews = null;
    this.updateForm.reset();
    this.deleteForm.reset();
  }

  private toNumber(value: any): number | null {
    if (value === null || value === undefined || value === '') {
      return null;
    }
    return Number(value);
  }

  private toIsoDateTime(value: any): string | null {
    if (!value) {
      return null;
    }
    const date = new Date(value);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}T00:00:00`;
  }

  private handleError(error: any, fallback: string): void {
    const message = error?.error?.errorDetail?.message ?? fallback;
    this.toastr.error(message);
  }
}