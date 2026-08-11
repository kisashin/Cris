<div>
    <div class="container-title">
        <h1 class="title">NOVEDADES INDIVIDUALES DE MOVIMIENTOS</h1>
    </div>

    <form class="product-search-form" [formGroup]="searchForm" (ngSubmit)="onSearch()">
        <div class="form-wrapper">
            <mat-form-field appearance="fill" floatLabel="always" class="product-field">
                <mat-label>Numero de Siniestro</mat-label>
                <input matInput type="text" formControlName="claimNumber" maxlength="70"
                    placeholder="Ingrese el numero de siniestro" autocomplete="off" />
                <mat-icon matSuffix>search</mat-icon>
            </mat-form-field>

            <button mat-raised-button color="primary" type="submit" [disabled]="searchForm.invalid"
                class="search-button">
                <mat-icon>search</mat-icon>
                Buscar
            </button>
        </div>
    </form>

    <hr>

    @if (showMovements) {
    <div class="container-table">
        <h2 class="subtitle">Movimientos del siniestro</h2>
        <app-report-table [dataSource]="movements" [displayedColumns]="movementColumns"></app-report-table>
    </div>
    }

    @if (showUpdateForm) {
    <form class="product-search-form" [formGroup]="updateForm" (ngSubmit)="onSaveUpdate()">
        <h2 class="subtitle">Solicitud de actualizacion</h2>
        <div class="form-wrapper">

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Tipo movimiento</mat-label>
                <input matInput type="text" formControlName="movementType" maxlength="100" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Socio</mat-label>
                <input matInput type="text" formControlName="partner" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Tipo Coaseguro</mat-label>
                <input matInput type="number" formControlName="coinsuranceType" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Valor Coaseguro Retenido</mat-label>
                <input matInput type="number" formControlName="retainedCoinsuranceValue" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Valor Coaseguro Cedido</mat-label>
                <input matInput type="number" formControlName="cededCoinsuranceValue" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Cobertura</mat-label>
                <input matInput type="text" formControlName="coverage" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Id Cardif</mat-label>
                <input matInput type="text" formControlName="cardifId" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Llave Siniestro</mat-label>
                <input matInput type="text" formControlName="claimKey" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Ramo</mat-label>
                <input matInput type="text" formControlName="branchCode" maxlength="120" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Numero Siniestro</mat-label>
                <input matInput type="text" formControlName="claimNumber" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Beneficiario Pago</mat-label>
                <input matInput type="text" formControlName="paymentBeneficiary" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Cod Socio</mat-label>
                <input matInput type="number" formControlName="partnerCode" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Estado Siniestro</mat-label>
                <input matInput type="text" formControlName="claimStatus" maxlength="100" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Estado Mayor</mat-label>
                <input matInput type="text" formControlName="majorStatus" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Canal</mat-label>
                <input matInput type="text" formControlName="channel" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Pandemia</mat-label>
                <input matInput type="text" formControlName="pandemic" maxlength="255" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha Aviso Socio</mat-label>
                <input matInput [matDatepicker]="pickerPartner" formControlName="partnerNoticeDate" />
                <mat-datepicker-toggle matSuffix [for]="pickerPartner"></mat-datepicker-toggle>
                <mat-datepicker #pickerPartner></mat-datepicker>
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha Aviso Cardif</mat-label>
                <input matInput [matDatepicker]="pickerCardif" formControlName="cardifNoticeDate" />
                <mat-datepicker-toggle matSuffix [for]="pickerCardif"></mat-datepicker-toggle>
                <mat-datepicker #pickerCardif></mat-datepicker>
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha Ocurrencia</mat-label>
                <input matInput [matDatepicker]="pickerOccurrence" formControlName="occurrenceDate" />
                <mat-datepicker-toggle matSuffix [for]="pickerOccurrence"></mat-datepicker-toggle>
                <mat-datepicker #pickerOccurrence></mat-datepicker>
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Fecha Nacimiento</mat-label>
                <input matInput [matDatepicker]="pickerBirth" formControlName="birthDate" />
                <mat-datepicker-toggle matSuffix [for]="pickerBirth"></mat-datepicker-toggle>
                <mat-datepicker #pickerBirth></mat-datepicker>
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Justificacion del cambio</mat-label>
                <input matInput type="text" formControlName="justification" maxlength="255" />
            </mat-form-field>

            <button mat-raised-button color="primary" type="submit" [disabled]="updateForm.invalid"
                class="search-button">
                Guardar
            </button>
        </div>
    </form>
    }

    @if (showDeleteForm) {
    <form class="product-search-form" [formGroup]="deleteForm" (ngSubmit)="onSaveDelete()">
        <h2 class="subtitle">Solicitud de eliminacion</h2>
        <div class="form-wrapper">

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Tipo movimiento</mat-label>
                <input matInput type="text" formControlName="movementType" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Socio</mat-label>
                <input matInput type="text" formControlName="partner" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Cobertura</mat-label>
                <input matInput type="text" formControlName="coverage" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Ramo</mat-label>
                <input matInput type="text" formControlName="branchCode" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Numero Siniestro</mat-label>
                <input matInput type="text" formControlName="claimNumber" />
            </mat-form-field>

            <mat-form-field appearance="fill" class="product-field">
                <mat-label>Justificacion del borrado</mat-label>
                <input matInput type="text" formControlName="justification" maxlength="255" />
            </mat-form-field>

            <button mat-raised-button color="warn" type="submit" [disabled]="deleteForm.invalid"
                class="search-button">
                Eliminar
            </button>
        </div>
    </form>
    }

    @if (selectedNews) {
    <div class="container-detail">
        <h2 class="subtitle">Detalle de la novedad</h2>
        <ul>
            <li><strong>Codigo:</strong> {{ selectedNews.code }}</li>
            <li><strong>ID Carvajal:</strong> {{ selectedNews.idCarvajal }}</li>
            <li><strong>Numero Siniestro:</strong> {{ selectedNews.claimNumber }}</li>
            <li><strong>Tipo Novedad:</strong> {{ selectedNews.newsType }}</li>
            <li><strong>Estado:</strong> {{ selectedNews.status }}</li>
            <li><strong>Justificacion:</strong> {{ selectedNews.justification }}</li>
            <li><strong>Fecha Proceso:</strong> {{ selectedNews.processDate }}</li>
            <li><strong>Solicitante:</strong> {{ selectedNews.requestUser }}</li>
        </ul>
        <button mat-raised-button (click)="selectedNews = null">Cerrar</button>
    </div>
    }

    <hr>

    <div class="container-table">
        <h2 class="subtitle">NOVEDADES POR AUTORIZAR</h2>
        <app-report-table [dataSource]="pendingNews" [displayedColumns]="newsColumns"></app-report-table>
    </div>
</div>