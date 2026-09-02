import java.util.Date;

import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
    
    
    
    public static final String USER = "j36147";
    public static final String XML_CONTENT = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC/>";
    public static final String FILE_NAME = "2012_202602SINIE_2012202602.XML";



        public static SendAccountingRequestDto sendRequest() {
        SendAccountingRequestDto request = new SendAccountingRequestDto();
        request.setProduct(PRODUCT);
        request.setComment(COMMENT);
        request.setUser(USER);
        return request;
    }


        public static XmlFileDto xmlFile(String journalType) {
        return new XmlFileDto(journalType, journalType + "_" + PRODUCT + ".XML", XML_CONTENT);
    }

    public static Object[] xmlRow() {
        return new Object[] { "SINIE", FILE_NAME, XML_CONTENT };
    }

    public static Object[] fileRow() {
        return new Object[] { 1, PRODUCT, "SINIE", FILE_NAME, new Date() };
    }
