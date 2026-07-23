<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN" monitorInterval="30">
	<Properties>
		<Property name="LOG_PATTERN">%d{yyyy-MM-dd'T'HH:mm:ss.SSSZ} ${hostName} %p %m%n</Property>
        <Property name="serviceVersion">${bundle:application:bnp.versionProyect}</Property>
        <Property name="serviceName">${bundle:application:bnp.projectName}</Property>
		<Property name="ROOT_FILE">logs</Property>
	</Properties>
	<Appenders>
		<Console name="Console" target="SYSTEM_OUT" follow="true">
            <JsonTemplateLayout
                    eventTemplateUri="classpath:JsonTemplate.json">
            </JsonTemplateLayout>
		</Console>

		<!-- ============================================================= -->
		<!-- TEMPORAL - BORRAR DESPUES DE LAS PRUEBAS                      -->
		<!-- Appender de texto plano para ver el stack trace completo.     -->
		<!-- JsonTemplate.json usa field="className" en error.stack_trace, -->
		<!-- por lo que NO imprime las causas y el mensaje real de         -->
		<!-- SQL Server queda oculto dentro de la excepcion de Hibernate.  -->
		<!-- %throwable si imprime la cadena completa de "Caused by".      -->
		<!-- ============================================================= -->
		<Console name="DebugTemporal" target="SYSTEM_OUT" follow="true">
			<PatternLayout pattern="%d{HH:mm:ss.SSS} %-5p %c{1}.%M - %m%n%throwable"/>
		</Console>
		<!-- ============ FIN BLOQUE TEMPORAL - BORRAR ==================== -->

		<RollingFile name="appLog" fileName="${ROOT_FILE}/LogWsCierres.log" filePattern="${ROOT_FILE}/LogWsCierres-%d{yyyy-MM-dd}-%i.log">
			<LevelRangeFilter minLevel="ERROR" maxLevel="ERROR" onMatch="ACCEPT" onMismatch="DENY" />
            <JsonTemplateLayout
                    eventTemplateUri="classpath:JsonTemplate.json">
            </JsonTemplateLayout>
			<Policies>
				<SizeBasedTriggeringPolicy size="19500KB" />
			</Policies>
			<DefaultRolloverStrategy max="1" />
		</RollingFile>
		<RollingFile name="appTraza" fileName="${ROOT_FILE}/TrazaWsCierres.log" filePattern="${ROOT_FILE}/TrazaWsCierres-%d{yyyy-MM-dd}-%i.log">
			<LevelRangeFilter minLevel="INFO" maxLevel="INFO" onMatch="ACCEPT" onMismatch="DENY" />
            <JsonTemplateLayout
                    eventTemplateUri="classpath:JsonTemplate.json">
            </JsonTemplateLayout>
			<Policies>
				<SizeBasedTriggeringPolicy size="19500KB" />
			</Policies>
			<DefaultRolloverStrategy max="1" />
		</RollingFile>
	</Appenders>
	<Loggers>

		<!-- ============================================================= -->
		<!-- TEMPORAL - BORRAR DESPUES DE LAS PRUEBAS                      -->
		<!-- additivity="true": ademas del texto plano, los eventos siguen -->
		<!-- llegando al Root, asi que los archivos JSON se siguen         -->
		<!-- alimentando igual que siempre. Efecto: cada linea aparece dos -->
		<!-- veces en consola (una JSON, una texto plano). Si molesta,     -->
		<!-- cambiar a additivity="false", pero entonces las trazas de     -->
		<!-- este paquete NO quedan en LogWsCierres.log ni TrazaWsCierres. -->
		<!-- ============================================================= -->
		<Logger name="co.com.bnpparibas.cardif.cierres" level="info" additivity="true">
			<AppenderRef ref="DebugTemporal"/>
		</Logger>
		<!-- ============ FIN BLOQUE TEMPORAL - BORRAR ==================== -->

		<Root level="info">
			<AppenderRef ref="Console" />
			<AppenderRef ref="appLog" />
			<AppenderRef ref="appTraza" />
		</Root>
	</Loggers>
</Configuration>
