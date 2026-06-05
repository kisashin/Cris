// HomologationPolicy.model.ts
// Se agrega id y aplicaVigencia — necesarios para editar y eliminar

export interface HomologationPolicy {
  id?: number;
  productCode: number;
  ramoCode: number;
  policyNumber: string;
  aplicaVigencia?: number;
  startDate: string | null;
  endDate: string | null;
}


<div>
    <div class="container-title">
        <h1 class="title">HOMOLOGACIÓN POLIZA ALFA</h1>
    </div>

    <!-- Formulario de búsqueda -->
    <form class="product-search-form" [formGroup]="productForm" (ngSubmit)="onSearch()">
        <div class="form-wrapper">
            <mat-form-field appearance="fill" floatLabel="always" class="product-field">
                <mat-label>Producto</mat-label>
                <input matInput id="product-input" type="text" formControlName="product"
                    placeholder="Ingrese producto" autocomplete="off" />
                <mat-icon matSuffix>search</mat-icon>
            </mat-form-field>

            <button mat-raised-button color="primary" type="submit" [disabled]="productForm.invalid"
                class="search-button">
                <mat-icon>search</mat-icon>
                Buscar
            </button>
        </div>
    </form>

    <hr>

    <div class="container-btn-new-record">
        <button mat-raised-button color="primary"
            (click)="showFormHomologationFormPolicy = !showFormHomologationFormPolicy; editingId = null; formHomologationFormPolicy.reset({ appliesValidity: { value: 'no' } })">
            Nuevo registro
        </button>
    </div>

    <div class="container-table">
        <app-report-table [dataSource]="this.dataSource"
            [displayedColumns]="this.displayedColumns"></app-report-table>
    </div>

    <!-- Formulario de creación / edición -->
    @if (showFormHomologationFormPolicy) {
    <form class="product-search-form" [formGroup]="formHomologationFormPolicy" (ngSubmit)="onGuardar()">
        <div class="form-wrapper">

            <!-- Código producto -->
            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Código producto</mat-label>
                <input matInput type="text" formControlName="productCode" placeholder="Ingrese código producto" />
            </mat-form-field>

            <!-- Código ramo -->
            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Código ramo</mat-label>
                <input matInput type="text" formControlName="ramoCode" placeholder="Ingrese código ramo" />
            </mat-form-field>

            <!-- Número de póliza -->
            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Número de póliza</mat-label>
                <input matInput type="text" formControlName="policyNumber"
                    placeholder="Ingrese número de póliza" />
            </mat-form-field>

            <!-- Aplica vigencia -->
            <div class="vigencia-group" formGroupName="appliesValidity">
                <label class="vigencia-label">Aplica vigencia:</label>
                <mat-radio-group formControlName="value">
                    <mat-radio-button value="no">No</mat-radio-button>
                    <mat-radio-button value="si">Sí</mat-radio-button>
                </mat-radio-group>
            </div>

            <!-- Fecha inicial -->
            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha inicial</mat-label>
                <input matInput [matDatepicker]="pickerStart" formControlName="startDate"
                    placeholder="dd/MM/yyyy" />
                <mat-datepicker-toggle matSuffix [for]="pickerStart"></mat-datepicker-toggle>
                <mat-datepicker #pickerStart></mat-datepicker>
            </mat-form-field>

            <!-- Fecha final -->
            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha final</mat-label>
                <input matInput [matDatepicker]="pickerEnd" formControlName="endDate"
                    placeholder="dd/MM/yyyy" />
                <mat-datepicker-toggle matSuffix [for]="pickerEnd"></mat-datepicker-toggle>
                <mat-datepicker #pickerEnd></mat-datepicker>
            </mat-form-field>

            @if (formHomologationFormPolicy.errors?.['dateRangeInvalid'] &&
            (formHomologationFormPolicy.get('startDate')?.touched ||
            formHomologationFormPolicy.get('endDate')?.touched)) {
            <div class="error-message">
                La fecha inicial no puede ser mayor que la fecha final.
            </div>
            }

            <!-- Botón guardar -->
            <button mat-raised-button color="primary" type="submit"
                [disabled]="formHomologationFormPolicy.invalid" class="search-button">
                Guardar
            </button>
        </div>
    </form>
    }
</div>

// src/app/views/claims-closing/movements-col/homologation-policy-alfa/homologation-policy-alfa.component.scss

.text-primary-color {
    color: #006600;
    font-family: Franklin Gothic Medium;
}

.container-title {
    padding-bottom: 3rem;

    .title {
        font-family: Franklin Gothic Medium;
        color: #006600;
        font-size: 14pt;
    }
}

.product-search-form {
    width: 100%;
    max-width: 700px;
    margin-top: 1rem;
}

.form-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: flex-start;
}

.product-field {
    flex: 1 1 250px;
}

.search-button {
    height: 56px;
}

.container-btn-new-record {
    display: flex;
    align-items: flex-end;
    gap: 1rem;
    margin-bottom: 2rem;
}

.error-message {
    color: #D60000;
    font-size: 12px;
    margin-top: 4px;
    width: 100%;
}

.vigencia-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 160px;

    .vigencia-label {
        font-size: 12px;
        color: rgba(0, 0, 0, 0.6);
    }

    mat-radio-group {
        display: flex;
        gap: 12px;
    }
}

.form-actions {
    display: flex;
    gap: 12px;
    align-items: center;
    width: 100%;
    margin-top: 8px;
}

// src/app/views/claims-closing/movements-col/homologation-policy-alfa/homologation-policy-alfa.component.spec.ts

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { HomologationPolicyAlfaComponent } from './homologation-policy-alfa.component';
import { HomologationPolicyAlfaService } from './homologation-policy-alfa.service';
import { HomologationPolicy } from '../../models/HomologationPolicy.model';

const mockPolicy: HomologationPolicy = {
  id: 1,
  productCode: '1001',
  ramoCode: '24',
  policyNumber: '0000001',
  startDate: null,
  endDate: null,
  aplicaVigencia: 0
};

const mockServiceFactory = () => ({
  buscarPorProducto: jasmine.createSpy('buscarPorProducto').and.returnValue(of([mockPolicy])),
  crear:             jasmine.createSpy('crear').and.returnValue(of(mockPolicy)),
  editar:            jasmine.createSpy('editar').and.returnValue(of(mockPolicy)),
  eliminar:          jasmine.createSpy('eliminar').and.returnValue(of(void 0))
});

describe('HomologationPolicyAlfaComponent', () => {
  let component: HomologationPolicyAlfaComponent;
  let fixture: ComponentFixture<HomologationPolicyAlfaComponent>;
  let service: ReturnType<typeof mockServiceFactory>;

  beforeEach(async () => {
    service = mockServiceFactory();

    await TestBed.configureTestingModule({
      declarations: [HomologationPolicyAlfaComponent],
      imports: [ReactiveFormsModule],
      providers: [
        { provide: HomologationPolicyAlfaService, useValue: service }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(HomologationPolicyAlfaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('productForm debe ser inválido cuando está vacío', () => {
    expect(component.productForm.invalid).toBeTrue();
  });

  it('productForm debe ser válido con producto ingresado', () => {
    component.productForm.setValue({ product: '1001' });
    expect(component.productForm.valid).toBeTrue();
  });

  it('onSearch llama al servicio y carga el dataSource', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();
    expect(service.buscarPorProducto).toHaveBeenCalledWith('1001');
    expect(component.dataSource.length).toBe(1);
  });

  it('onSearch no llama al servicio si el formulario es inválido', () => {
    component.onSearch();
    expect(service.buscarPorProducto).not.toHaveBeenCalled();
  });

  it('nuevoRegistro muestra el formulario y limpia editingId', () => {
    component.nuevoRegistro();
    expect(component.showFormHomologationFormPolicy).toBeTrue();
    expect((component as any).editingId).toBeNull();
  });

  it('editMode carga los datos del registro en el formulario', () => {
    component.editMode(mockPolicy, 0);
    expect(component.showFormHomologationFormPolicy).toBeTrue();
    expect((component as any).editingId).toBe(1);
    expect(component.formHomologationFormPolicy.value.productCode).toBe('1001');
    expect(component.formHomologationFormPolicy.value.policyNumber).toBe('0000001');
  });

  it('onGuardar llama a crear cuando editingId es null', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();

    component.nuevoRegistro();
    component.formHomologationFormPolicy.setValue({
      productCode:     '1001',
      ramoCode:        '24',
      policyNumber:    '0000001',
      appliesValidity: { value: 'no' },
      startDate:       '2024-01-01',
      endDate:         '2024-12-31'
    });

    component.onGuardar();
    expect(service.crear).toHaveBeenCalled();
  });

  it('onGuardar llama a editar cuando editingId tiene valor', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();

    component.editMode(mockPolicy, 0);
    component.formHomologationFormPolicy.setValue({
      productCode:     '1001',
      ramoCode:        '24',
      policyNumber:    '0000001',
      appliesValidity: { value: 'no' },
      startDate:       '2024-01-01',
      endDate:         '2024-12-31'
    });

    component.onGuardar();
    expect(service.editar).toHaveBeenCalledWith(1, jasmine.any(Object));
  });

  it('deleteMode llama al servicio eliminar con el id correcto', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();
    component.deleteMode(mockPolicy, 0);
    expect(service.eliminar).toHaveBeenCalledWith(1);
  });

  it('deleteMode no llama al servicio si el registro no tiene id', () => {
    const sinId: HomologationPolicy = { ...mockPolicy, id: undefined };
    component.deleteMode(sinId, 0);
    expect(service.eliminar).not.toHaveBeenCalled();
  });

  it('dateRangeValidator retorna error si startDate > endDate', () => {
    component.formHomologationFormPolicy.patchValue({
      startDate: '2024-12-31',
      endDate:   '2024-01-01'
    });
    const errors = component.formHomologationFormPolicy.errors;
    expect(errors?.['dateRangeInvalid']).toBeTrue();
  });

  it('dateRangeValidator no retorna error si startDate <= endDate', () => {
    component.formHomologationFormPolicy.patchValue({
      startDate: '2024-01-01',
      endDate:   '2024-12-31'
    });
    const errors = component.formHomologationFormPolicy.errors;
    expect(errors).toBeNull();
  });

  it('muestra errorMessage cuando buscarPorProducto falla', () => {
    service.buscarPorProducto.and.returnValue(throwError(() => new Error('Error red')));
    component.productForm.setValue({ product: '1001' });
    component.onSearch();
    expect(component.errorMessage).toContain('Error al buscar');
  });
});


import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
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
  private editingId: number | null = null;

  public displayedColumns: IMetaColumn[] = [
    { title: 'Codigo Producto', field: 'productCode' },
    { title: 'Codigo ramo', field: 'ramoCode' },
    { title: 'Número poliza', field: 'policyNumber' },
    { title: 'Fecha Inicio', field: 'startDate' },
    { title: 'Fecha final', field: 'endDate' },
    {
      title: 'Acciones', field: 'actions', actions: [
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
        },
      ]
    },
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
      ramoCode: ['', Validators.required],
      policyNumber: ['', Validators.required],
      appliesValidity: this.fb.group({
        value: ['no', Validators.required]
      }),
      startDate: [''],
      endDate: ['']
    }, { validators: this.dateRangeValidator });
  }

  /** Validador que asegura que startDate <= endDate */
  dateRangeValidator: ValidatorFn = (group: AbstractControl): ValidationErrors | null => {
    const start = group.get('startDate')?.value;
    const end = group.get('endDate')?.value;
    if (start && end && new Date(start) > new Date(end)) {
      return { dateRangeInvalid: true };
    }
    return null;
  };

  onSearch(): void {
    if (this.productForm.valid) {
      const producto = Number(this.productForm.value.product);
      this.homologationPolicyAlfaSrv.buscarPorProducto(producto).subscribe({
        next: (response) => {
          if (response && response.bodyResponse) {
            this.dataSource = response.bodyResponse;
          }
        },
        error: (error) => {
          console.error('Error al buscar homologaciones:', error);
        }
      });
    }
  }

  onGuardar(): void {
    if (this.formHomologationFormPolicy.valid) {
      const formValue = this.formHomologationFormPolicy.value;
      const payload: HomologationPolicy = {
        productCode: Number(formValue.productCode),
        ramoCode: Number(formValue.ramoCode),
        policyNumber: formValue.policyNumber,
        aplicaVigencia: formValue.appliesValidity.value === 'si' ? 1 : 0,
        startDate: formValue.startDate || null,
        endDate: formValue.endDate || null
      };

      if (this.editingId) {
        this.homologationPolicyAlfaSrv.editar(this.editingId, payload).subscribe({
          next: () => {
            this.showFormHomologationFormPolicy = false;
            this.editingId = null;
            this.onSearch();
          },
          error: (error) => {
            console.error('Error al editar homologación:', error);
          }
        });
      } else {
        this.homologationPolicyAlfaSrv.crear(payload).subscribe({
          next: () => {
            this.showFormHomologationFormPolicy = false;
            this.onSearch();
          },
          error: (error) => {
            console.error('Error al crear homologación:', error);
          }
        });
      }
    }
  }

  editMode(policy: HomologationPolicy, index: number) {
    this.editingId = policy.id ?? null;
    this.showFormHomologationFormPolicy = true;
    this.formHomologationFormPolicy.patchValue({
      productCode: policy.productCode,
      ramoCode: policy.ramoCode,
      policyNumber: policy.policyNumber,
      appliesValidity: { value: policy.aplicaVigencia === 1 ? 'si' : 'no' },
      startDate: policy.startDate,
      endDate: policy.endDate
    });
  }

  deleteMode(row: HomologationPolicy, index: number) {
    if (row.id) {
      this.homologationPolicyAlfaSrv.eliminar(row.id).subscribe({
        next: () => {
          this.onSearch();
        },
        error: (error) => {
          console.error('Error al eliminar homologación:', error);
        }
      });
    }
  }
}

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { INewGeneralResponse } from '../models/new-general-response.interface';
import { HomologationPolicy } from '../models/HomologationPolicy.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class HomologationPolicyAlfaService {

  private readonly baseUrl = `${environment.urlAPIClosingClaimsBackEnd}`;

  constructor(private http: HttpClient) { }

  /**
   * Busca registros de homologación por código de producto.
   * Equivalente a CargarGridView1 del legacy.
   *
   * @param producto Código de producto a buscar.
   * @returns Observable con la lista de registros encontrados.
   */
  buscarPorProducto(producto: number): Observable<INewGeneralResponse<HomologationPolicy[]>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
    const params = new HttpParams().set('producto', producto.toString());
    return this.http.get<INewGeneralResponse<HomologationPolicy[]>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa`,
      { headers, params }
    );
  }

  /**
   * Crea un nuevo registro de homologación.
   * Equivalente a BtnGuardar_Click con id = 0 del legacy.
   *
   * @param data Datos del nuevo registro.
   * @returns Observable con el registro creado.
   */
  crear(data: HomologationPolicy): Observable<INewGeneralResponse<HomologationPolicy>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
    return this.http.post<INewGeneralResponse<HomologationPolicy>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa`,
      data,
      { headers }
    );
  }

  /**
   * Edita un registro existente de homologación.
   * Equivalente a BtnGuardar_Click con id != 0 del legacy.
   *
   * @param id   Identificador del registro a editar.
   * @param data Datos actualizados.
   * @returns Observable con el registro actualizado.
   */
  editar(id: number, data: HomologationPolicy): Observable<INewGeneralResponse<HomologationPolicy>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
    return this.http.put<INewGeneralResponse<HomologationPolicy>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa/${id}`,
      data,
      { headers }
    );
  }

  /**
   * Elimina un registro de homologación por su id.
   * Equivalente a btnEliminar_Click del legacy.
   *
   * @param id Identificador del registro a eliminar.
   * @returns Observable con la respuesta del servidor.
   */
  eliminar(id: number): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', crypto.randomUUID());
    return this.http.delete<INewGeneralResponse<string>>(
      `${this.baseUrl}/v1/homologacion-poliza-alfa/${id}`,
      { headers }
    );
  }
}

