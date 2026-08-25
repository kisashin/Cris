import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

import { ConfirmDialogComponent } from './confirm-dialog.component';
import { IConfirmDialogData } from './confirm-dialog.model';

describe('ConfirmDialogComponent', () => {
  let component: ConfirmDialogComponent;
  let fixture: ComponentFixture<ConfirmDialogComponent>;
  let dialogRef: jasmine.SpyObj<MatDialogRef<ConfirmDialogComponent>>;

  const createComponent = async (data: IConfirmDialogData) => {
    dialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.resetTestingModule()
      .configureTestingModule({
        imports: [ConfirmDialogComponent],
        providers: [
          { provide: MatDialogRef, useValue: dialogRef },
          { provide: MAT_DIALOG_DATA, useValue: data }
        ]
      })
      .compileComponents();

    fixture = TestBed.createComponent(ConfirmDialogComponent);
    component = fixture.componentInstance;
  };

  it('should create with the provided data', async () => {
    await createComponent({
      title: 'Generar nuevo XML',
      message: 'Se borrarán los registros anteriores.',
      confirmText: 'SÍ, GENERAR',
      cancelText: 'CANCELAR'
    });

    expect(component).toBeTruthy();
    expect(component.data.title).toBe('Generar nuevo XML');
    expect(component.confirmText).toBe('SÍ, GENERAR');
    expect(component.cancelText).toBe('CANCELAR');
  });

  it('should fall back to the default button labels', async () => {
    await createComponent({
      title: 'Confirmar',
      message: '¿Desea continuar?'
    });

    expect(component.confirmText).toBe('SÍ');
    expect(component.cancelText).toBe('NO');
  });

  it('should close with true when confirmed', async () => {
    await createComponent({ title: 'Confirmar', message: 'Mensaje' });

    component.confirm();

    expect(dialogRef.close).toHaveBeenCalledWith(true);
  });

  it('should close with false when cancelled', async () => {
    await createComponent({ title: 'Confirmar', message: 'Mensaje' });

    component.cancel();

    expect(dialogRef.close).toHaveBeenCalledWith(false);
  });
});
