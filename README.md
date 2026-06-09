import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { HomologationPolicyAlfaComponent } from './homologation-policy-alfa.component';
import { HomologationPolicyAlfaService } from '../../services/homologation-policy-alfa.service';
import { HomologationPolicy } from '../../models/HomologationPolicy.model';

const mockPolicy: HomologationPolicy = {
  id: 1,
  productCode: 1001,
  branchCode: 24,
  policyNumber: '0000001',
  startDate: null,
  endDate: null,
  appliesValidity: 0
};

const mockServiceFactory = () => ({
  buscarPorProducto: jasmine.createSpy('buscarPorProducto')
    .and.returnValue(of({ bodyResponse: [mockPolicy] } as any)),
  crear: jasmine.createSpy('crear')
    .and.returnValue(of({ bodyResponse: mockPolicy } as any)),
  editar: jasmine.createSpy('editar')
    .and.returnValue(of({ bodyResponse: mockPolicy } as any)),
  eliminar: jasmine.createSpy('eliminar')
    .and.returnValue(of({ bodyResponse: null } as any))
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
    expect(service.buscarPorProducto).toHaveBeenCalledWith(1001);
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
    expect(component.formHomologationFormPolicy.value.productCode).toBe(1001);
    expect(component.formHomologationFormPolicy.value.policyNumber).toBe('0000001');
  });

  it('onGuardar llama a crear cuando editingId es null', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();

    component.nuevoRegistro();
    component.formHomologationFormPolicy.setValue({
      productCode: '1001',
      branchCode: '24',
      policyNumber: '0000001',
      appliesValidity: { value: 'no' },
      startDate: '2024-01-01',
      endDate: '2024-12-31'
    });

    component.onGuardar();
    expect(service.crear).toHaveBeenCalled();
  });

  it('onGuardar llama a editar cuando editingId tiene valor', () => {
    component.productForm.setValue({ product: '1001' });
    component.onSearch();

    component.editMode(mockPolicy, 0);
    component.formHomologationFormPolicy.setValue({
      productCode: '1001',
      branchCode: '24',
      policyNumber: '0000001',
      appliesValidity: { value: 'no' },
      startDate: '2024-01-01',
      endDate: '2024-12-31'
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
      endDate: '2024-01-01'
    });
    const errors = component.formHomologationFormPolicy.errors;
    expect(errors?.['dateRangeInvalid']).toBeTrue();
  });

  it('dateRangeValidator no retorna error si startDate <= endDate', () => {
    component.formHomologationFormPolicy.patchValue({
      startDate: '2024-01-01',
      endDate: '2024-12-31'
    });
    const errors = component.formHomologationFormPolicy.errors;
    expect(errors).toBeNull();
  });

  it('muestra errorMessage cuando buscarPorProducto falla', () => {
    service.buscarPorProducto.and.returnValue(
      throwError(() => new Error('Error red'))
    );
    component.productForm.setValue({ product: '1001' });
    component.onSearch();
    expect(component.errorMessage).toContain('Error al buscar');
  });
});
