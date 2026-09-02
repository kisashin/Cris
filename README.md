.upload-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.file-input {
  display: none;
}

.file-name {
  color: #333333;
  font-family: Arial, sans-serif;
  font-size: 13px;
  font-style: italic;
}

.files-section {
  width: 100%;
  margin-top: 2.5rem;

  .section-label {
    display: block;
    margin-bottom: 1rem;
  }

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

.action-button {
  mat-icon {
    margin-right: 6px;
  }
}
