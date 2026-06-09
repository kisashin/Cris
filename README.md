import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';

import { IMetaColumn } from '../../models/IMetaColumn.models';
import { HomologationPolicy } from '../../models/HomologationPolicy.model';
import { HomologationPolicyAlfaService } from '../../services/homologation-policy-alfa.service';

@Component({
  selector: 'app-homologation-policy-alfa',
  templateUrl: './homologation-policy-alfa.component.html',
  styleUrl: './homologation-policy-alfa.component.scss',
  standalone: false
})
export class HomologationPolicyAlfaComponent implements OnInit {

  public productForm!: FormGroup;
  public formHomologationFormPolicy!: FormGroup;
  public showFormHomologationFormPolicy: boolean = false;
  public editingId: number | null = null;
  public errorMessage: string = '';

  public displayedColumns: IMetaColumn[] = [
    { title: 'Codigo Producto', field: 'productCode' },
    { title: 'Codigo ramo', field: 'branchCode' },
    { title: 'Número poliza', field: 'policyNumber' },
    { title: 'Fecha Inicio', field: 'startDate' },
    { title: 'Fecha final', field: 'endDate' },
    {
      title: 'Acciones',
      field: 'actions',
      actions: [
        {
          action: (row: HomologationPolicy, index: number) => {
            this.editMode(row, index);
          },
          fasIcon: 'fal fa-edit',
          tooltip: () => 'Editar',
          isMenu: false,
          actionEditDeleteCircle: true,
          edit: true
        },
        {
          action: (row: HomologationPolicy, index: number) => {
            this.deleteMode(row, index);
          },
          fasIcon: 'fal fa-times-circle pointer',
          tooltip: () => 'Eliminar',
          isMenu: false,
          actionEditDeleteCircle: true,
          delete: true
        }
      ]
    }
  ];

  public dataSource: HomologationPolicy[] = [];

  constructor(
    private fb: FormBuilder,
    private homologationPolicyAlfaSrv: HomologationPolicyAlfaService
  ) { }

  ngOnInit(): void {
    this.productForm = this.fb.group({
      product: ['', Validators.required]
    });

    this.formHomologationFormPolicy = this.fb.group({
      productCode: ['', Validators.required],
      branchCode: ['', Validators.required],
      policyNumber: ['', Validators.required],
      appliesValidity: this.fb.group({
        value: ['no', Validators.required]
      }),
      startDate: [''],
      endDate: ['']
    }, { validators: this.dateRangeValidator });
  }

  /** Validador que asegura que startDate <= endDate */
  dateRangeValidator: ValidatorFn = (
    group: AbstractControl
  ): ValidationErrors | null => {

    const start = group.get('startDate')?.value;
    const end = group.get('endDate')?.value;

    if (start && end && new Date(start) > new Date(end)) {
      return { dateRangeInvalid: true };
    }

    return null;
  };

  onSearch(): void {
    if (this.productForm.valid) {
      const productCode = Number(
        this.productForm.value.product
      );

      this.errorMessage = '';

      this.homologationPolicyAlfaSrv
        .buscarPorProducto(productCode)
        .subscribe({
          next: (response) => {
            if (response && response.bodyResponse) {
              this.dataSource = response.bodyResponse.map(
                (item: any) => ({
                  id: item.id,
                  productCode: item.productCode,
                  branchCode: item.branchCode,
                  policyNumber: item.policyNumber,
                  appliesValidity: item.appliesValidity,
                  startDate: item.startDate,
                  endDate: item.endDate
                })
              );
            }
          },
          error: (error) => {
            console.error(
              'Error al buscar homologaciones:',
              error
            );

            this.errorMessage =
              'Error al buscar homologaciones';
          }
        });
    }
  }

  onGuardar(): void {
    if (this.formHomologationFormPolicy.valid) {
      const formValue =
        this.formHomologationFormPolicy.value;

      const payload: HomologationPolicy = {
        productCode: Number(
          formValue.productCode
        ),
        branchCode: Number(
          formValue.branchCode
        ),
        policyNumber:
          formValue.policyNumber,
        appliesValidity:
          formValue.appliesValidity.value === 'si'
            ? 1
            : 0,
        startDate: this.formatDate(
          formValue.startDate
        ),
        endDate: this.formatDate(
          formValue.endDate
        )
      };

      if (this.editingId !== null) {
        this.homologationPolicyAlfaSrv
          .editar(this.editingId, payload)
          .subscribe({
            next: () => {
              this.showFormHomologationFormPolicy =
                false;

              this.editingId = null;
              this.onSearch();
            },
            error: (error) => {
              console.error(
                'Error al editar homologación:',
                error
              );
            }
          });
      } else {
        this.homologationPolicyAlfaSrv
          .crear(payload)
          .subscribe({
            next: () => {
              this.showFormHomologationFormPolicy =
                false;

              this.onSearch();
            },
            error: (error) => {
              console.error(
                'Error al crear homologación:',
                error
              );
            }
          });
      }
    }
  }

  editMode(
    policy: HomologationPolicy,
    index: number
  ): void {

    this.editingId =
      policy.id ?? null;

    this.showFormHomologationFormPolicy =
      true;

    this.formHomologationFormPolicy.patchValue({
      productCode: policy.productCode,
      branchCode: policy.branchCode,
      policyNumber: policy.policyNumber,
      appliesValidity: {
        value:
          policy.appliesValidity === 1
            ? 'si'
            : 'no'
      },
      startDate: policy.startDate,
      endDate: policy.endDate
    });
  }

  deleteMode(
    row: HomologationPolicy,
    index: number
  ): void {

    if (row.id) {
      this.homologationPolicyAlfaSrv
        .eliminar(row.id)
        .subscribe({
          next: () => {
            this.onSearch();
          },
          error: (error) => {
            console.error(
              'Error al eliminar homologación:',
              error
            );
          }
        });
    }
  }

  nuevoRegistro(): void {
    this.showFormHomologationFormPolicy =
      true;

    this.editingId = null;

    this.formHomologationFormPolicy.reset({
      productCode: '',
      branchCode: '',
      policyNumber: '',
      appliesValidity: {
        value: 'no'
      },
      startDate: '',
      endDate: ''
    });
  }

  private formatDate(
    date: any
  ): string | null {

    if (!date) {
      return null;
    }

    const d = new Date(date);
    const year = d.getFullYear();

    const month = String(
      d.getMonth() + 1
    ).padStart(2, '0');

    const day = String(
      d.getDate()
    ).padStart(2, '0');

    return `${year}-${month}-${day}`;
  }
}
