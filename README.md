    private String formatMoney(BigDecimal value) {
        return value
                .setScale(MONEY_SCALE, RoundingMode.HALF_UP)
                .toPlainString()
                .replace('.', ',');
    }
