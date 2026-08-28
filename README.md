.accounting-report-container {
  width: 100%;
  max-width: 1100px;
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

.action-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.section-label {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 600;
  font-size: 14px;
}

.empty-message {
  color: #666666;
  font-family: Arial, sans-serif;
  font-size: 13px;
  margin-bottom: 2rem;
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

.container-table {
  overflow-x: auto;
  padding-top: 0.5rem;
  margin-bottom: 2rem;

  table {
    width: 100%;
  }

  th.mat-mdc-header-cell,
  th.mat-header-cell {
    background-color: #14532d !important;
    color: #ffffff !important;
    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.03rem;
    padding: 0.9rem 0.75rem;
    text-align: center;
  }

  td.mat-mdc-cell,
  td.mat-cell {
    border-bottom: 1px solid #e0e0e0;
    font-family: Arial, sans-serif;
    font-size: 13px;
    padding: 0.75rem;
    text-align: center;
  }

  .download-link {
    color: #1976d2 !important;
    cursor: pointer;
    font-family: Arial, sans-serif;
    text-decoration: underline;

    &:hover {
      color: #0d47a1 !important;
    }
  }
}

@media (max-width: 768px) {
  .accounting-report-container {
    padding: 1rem;
  }

  .container-title {
    padding-bottom: 2rem;
  }

  .action-section {
    align-items: flex-start;
    flex-direction: column;
    gap: 1rem;
  }

  .action-button,
  .download-button {
    width: 100%;
  }
}
