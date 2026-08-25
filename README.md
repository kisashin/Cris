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

.container-actions {
    align-items: center;
    display: flex;
    padding-bottom: 1.5rem;

    .text-primary-color {
        min-width: 18rem;
    }
}

.action-button {
    background-color: #14532d;
    border-radius: 2rem;
    color: #ffffff;
    font-family: Franklin Gothic Medium;
    letter-spacing: 0.05rem;
    padding: 0 1.75rem;

    mat-icon {
        margin-right: 0.5rem;
        vertical-align: middle;
    }

    &:disabled {
        background-color: #9e9e9e;
        color: #ffffff;
    }
}

.container-table {
    padding-top: 1.5rem;

    table {
        width: 100%;
    }

    th.mat-mdc-header-cell {
        background-color: #14532d;
        color: #ffffff;
        font-family: Franklin Gothic Medium;
        font-size: 11pt;
        font-weight: bold;
        letter-spacing: 0.03rem;
        padding: 0.9rem 0.75rem;
        text-align: center;
    }

    td.mat-mdc-cell {
        border-bottom: 1px solid #e0e0e0;
        padding: 0.75rem;
        text-align: center;
    }
}

.download-link {
    color: #006600;
    cursor: pointer;
    text-decoration: none;

    &:hover {
        text-decoration: underline;
    }
}
