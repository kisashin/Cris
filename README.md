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
                <input matInput type="text" formControlName="branchCode" placeholder="Ingrese código ramo" />
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
