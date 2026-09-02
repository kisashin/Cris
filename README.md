    @Transactional(transactionManager = "transactionManager", rollbackFor = Exception.class)
    public SendResponseDto sendEntry(SendAccountingRequestDto request) {



        @Transactional(transactionManager = "transactionManager", readOnly = true)
    public List<AccountingFileDto> getFiles() {


        @Transactional(transactionManager = "transactionManager", readOnly = true)
    public DownloadFileDto downloadFile(Integer id) {
