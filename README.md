src/app/views/claims-closing/movements-peru/peru-accounting-report/peru-accounting-report.component.scss

.accounting-report-container {
  width: 100%;
  max-width: 900px;
  padding: 1rem 0;
}

.container-title {
  padding-bottom: 3rem;

  .title {
    margin: 0;
    color: #006600;
    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
    font-size: 14pt;
    font-weight: 600;
  }
}

.generation-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.section-label,
.section-title {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 600;
}

.section-label {
  font-size: 14px;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 14px;
}

.action-button,
.download-button {
  min-height: 40px;
  padding: 0 1.25rem;
  color: #ffffff !important;
  background-color: #006600 !important;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 500;
  text-transform: uppercase;

  mat-icon {
    margin-right: 6px;
  }

  &:hover:not(:disabled) {
    background-color: #004d00 !important;
  }

  &:disabled {
    color: rgba(255, 255, 255, 0.7) !important;
    background-color: #7aa87a !important;
    cursor: not-allowed;
  }
}

.error-message {
  width: 100%;
  max-width: 700px;
  margin: 0 0 1.5rem;
  padding: 0.75rem 1rem;
  color: #a40000;
  background-color: #fdeaea;
  border: 1px solid #d60000;
  border-radius: 4px;
  font-size: 13px;
}

.previous-report-section {
  width: 100%;
  margin-top: 1rem;
}

.report-table-container {
  width: 100%;
  overflow-x: auto;
}

.report-table {
  width: 100%;
  min-width: 580px;
  border-collapse: collapse;
  font-family: Arial, sans-serif;
  font-size: 13px;

  th,
  td {
    padding: 12px 16px;
    border: 1px solid #c5cecc;
    text-align: center;
    vertical-align: middle;
  }

  th {
    color: #ffffff;
    background-color: #1c5e55;
    font-weight: 600;
  }

  tbody tr {
    background-color: #e3eaeb;
  }

  tbody tr:hover {
    background-color: #d4e0df;
  }

  td:first-child {
    min-width: 230px;
  }

  td:last-child {
    min-width: 230px;
  }
}

@media (max-width: 768px) {
  .accounting-report-container {
    padding: 1rem;
  }

  .container-title {
    padding-bottom: 2rem;
  }

  .generation-section {
    align-items: flex-start;
    flex-direction: column;
    gap: 1rem;
  }

  .action-button,
  .download-button {
    width: 100%;
  }
}

src/app/app-routing.module.ts

import { PeruAccountingReportComponent } from './views/claims-closing/movements-peru/peru-accounting-report/peru-accounting-report.component';

{
  path: 'peru-accounting-report',
  component: PeruAccountingReportComponent,
  canActivate: [AuthenticateGuardian],
  data: {
    menuKey: 'ClaimsClosing'
  }
},




{
  path: 'load-movements-peru',
  component: LoadMovementsPeruComponent,
  canActivate: [AuthenticateGuardian],
  data: {
    menuKey: 'ClaimsClosing'
  }
},
{
  path: 'peru-accounting-report',
  component: PeruAccountingReportComponent,
  canActivate: [AuthenticateGuardian],
  data: {
    menuKey: 'ClaimsClosing'
  }
},
