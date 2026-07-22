import { Component, Input, OnChanges, OnInit, Output, EventEmitter } from '@angular/core';
import { IMetaColumn } from '../../models/IMetaColumn.models';

@Component({
  selector: 'app-report-table',
  templateUrl: './report-table.component.html',
  styleUrl: './report-table.component.scss',
  standalone: false
})
export class ReportTableComponent implements OnInit, OnChanges {

  @Input({ required: true }) displayedColumns!: IMetaColumn[];
  @Input({ required: true }) dataSource!: any[];
  @Input() public pageSize: number = 0;
  @Input() public pageIndex: number = 0;

  @Output() actionClick = new EventEmitter<any>();

  public listFields: any[];

  ngOnInit(): void {
    this.buildFields();
  }

  ngOnChanges(): void {
    this.buildFields();
  }

  onAction(row: any): void {
    this.actionClick.emit(row);
  }

  private buildFields(): void {
    this.listFields = this.displayedColumns.map((el) => el.field);
  }

}



<div class="table-responsive">
    <table mat-table [dataSource]="dataSource" class="mat-elevation-z8">
        <!-- Columnas dinámicas -->
        @for (column of displayedColumns; track column.field) {
        <ng-container [matColumnDef]="column.field">
            <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> {{ column.title }} </th>
            <td mat-cell *matCellDef="let element;  let dIndex = dataIndex">
                @if(column.actions){
                @for (item of column.actions; track $index) {
                @if (item.isButton) {
                <button mat-button (click)="onAction(element)">
                     {{ element[column.field] }} 
                </button>
                }
                @if (item.isLink) {
                <a href="{{item.href}}{{element[column.field]}}">{{ element[column.field] }}</a>
                }
                <!--acciones -->
                @if (item.edit) {
                <button mat-icon-button color="primary" [matTooltip]="item.tooltip ? item.tooltip(element) : ''" (click)="item.action(element, dIndex)" aria-label="Editar">
                    <mat-icon>edit</mat-icon>
                </button>
                }
                @if (item.delete) {
                <button mat-icon-button color="warn" [matTooltip]="item.tooltip ? item.tooltip(element) : ''" (click)="item.action(element, dIndex)" aria-label="Eliminar">
                    <mat-icon>delete</mat-icon>
                </button>
                }
                @if (item.isInsert) {
                    <button mat-icon-button color="primary" [matTooltip]="item.tooltip ? item.tooltip(element) : ''" (click)="item.action(element, dIndex)" aria-label="Eliminar">
                    <mat-icon>insert_chart_outlined</mat-icon>
                </button>
                }
                }
                } @else if(column.field === 'reportsCA' ) {
                <button mat-button>Rpt Datos</button>
                <button mat-button>Rpt Movimientos</button>
                }@else{
                {{ element[column.field] }}
                }
            </td>
        </ng-container>
        }
        <!-- Encabezado y Filas -->
        <tr mat-header-row *matHeaderRowDef="listFields"></tr>
        <tr mat-row *matRowDef="let row; columns: listFields;"></tr>
    </table>
</div>
