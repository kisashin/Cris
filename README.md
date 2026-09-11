import { Component, HostListener, OnInit,OnChanges } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { AutenticacionService } from '../login/service/autenticacion.service';
import { environment } from 'src/environments/environment';

@Component({
    selector: 'app-nav-bar',
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.css'],
    standalone: false
})
export class NavBarComponent implements OnInit,OnChanges {
  rutaActiva: string = ''; // Guarda la ruta seleccionada
  public bandReportes: boolean = false;
  public bandNovedades: boolean = false;
  dropdownActivo: string | null = null;
  /*
  Como Usar
  ruta?: // Ruta de navegación (opcional para dropdowns)
     icon:   // Icono de Material Icons
     tooltip: // Descripción emergente
      // Lista de submenús (opcional)
     submenu?:{
        titulo: string;  // Nombre del submenú
        ruta: string;    // Ruta a la que navega el submenú
        external: true  (opcinal) si es para abrir en una nueva pestaña,
        }
     ¨*/
  menuItemsCierres  = [
    { ruta: '/app-picker', icon: 'view_list', tooltip: 'Seleccion de app'},
    { ruta: '/home', icon: 'home', tooltip: 'Inicio' },
    { ruta: '/administration/general-params', icon: 'assignment', tooltip: 'Estatus de ejecución de procesos asíncronos' },
    { ruta: '/administration/cierres-config', icon: 'settings', tooltip: 'Configuracion' },
    { ruta: '/vistosbuenos', icon: 'verified', tooltip: 'Vistos Buenos' },
    { ruta: '/cargueEmisiones', icon: 'upload_file', tooltip: 'Cargue de Emisiones' },
    { ruta: '/MatrizCondiciones', icon: 'fact_check', tooltip: 'Matriz de Condiciones' },
    { ruta: '/modifCargue', icon: 'edit_document', tooltip: 'Modificacion de Cargue' },
    { ruta: '/habilitarValidacion', icon: 'dangerous', tooltip: 'Habilitar Validación' },
    { ruta: '/generacionCierreContable', icon: 'calculate', tooltip: 'Asientos Contables' },
    {
      ruta: 'reportes', icon: 'bar_chart', tooltip: 'Reportes',
      submenu: [
        //TODO: revisar y quitar los que sean rutas de la aplicacion y ponerlas aqui y las demas revisar a ver para ponerlas
    //en los demas enviroments y mejor utilizar el routeLink para las rutas de la app de cierres las demas si con href si es necesario
    {
      titulo: 'Auxiliar produccion',
      url: environment.urlReportingServAuxProd,
      external: true,
    },
    {
      titulo: 'Resumen historico',
      url: environment.urlReportingServRtHistResumen,
      external: true,
    },
    {
      titulo: 'Asientos cierre diario',
      url: environment.urlReportingServAsientosCierreD,
      external: true,
    },
    {
      titulo: 'VoBo Cierre diario',
      url: environment.urlReportingServVBCierreD,
      external: true,
    },
    {
      titulo: 'Reporte diario ebilling',
      url: environment.urlDailyEbillingReport,
      external: true,
    },
    {
      titulo: 'Reporte ingresos facturas no conciliada',
      url: environment.urlIncomeReportInvoicesNotReconciled,
      external: true,
    },
    {
      titulo: 'Ingresos pendientes facturacion electronica',
      url: environment.urlPendingRevenueElectronicInvoicing,
      external: true,
    },
    {
      titulo: 'Polizas ebilling no cierre',
      url: environment.urlEbillingPoliciesDoNotClose,
      external: true,
    },
    {
      titulo: 'Reporte consulta de cobros',
      url: environment.urlCollectionInquiryReport,
      external: true,
    },
    {
      titulo: 'Reporte cancelaciones Banco Agrario',
      url: environment.urlAgrarioCancelReport,
      external: true,
    },
    {
      titulo: 'Reporte cancealciones call center',
      url: environment.urlCallCenterCancelReport,
      external: true,
    },
    { titulo: 'Consulta masiva auxiliar', url: ['/ConsultaMasivaAux'] },
    { titulo: 'Reportes tomadatos', url: ['/tomaDatos'] },
    {
      titulo: 'Reversar provisionales',
      url: ['/reversarProvisionales'],
    },
    { titulo: 'Reversar asiento', url: ['/reversarAsiento'] },
    {
      titulo: 'Inserta provisional masivo',
      url: ['/provisionalMasivo'],
    },
      ]
    },
    {
      ruta: 'novedades', icon: 'insights', tooltip: 'Novedades',
      submenu: [
        {
          titulo: 'Novedades acumuladas',
          url: ['/automatizaciones/novedades-acumuladas'],
        },
        {
          titulo: 'Cargue coap a cierres',
          url: ['/automatizaciones/cargue-coap'],
        },
        // {
        //   titulo: 'CARGUE COBRA A CIERRES',
        //   url: ['/automatizaciones/cargue-cobra'],
        // }, TODO: se oculta momentiamente a peticion de michael vinasco
        {
          titulo: 'Actualizar TRM y generar tomadatos',
          url: ['/automatizaciones/trm-tomadatos'],
        },
        {
          titulo: 'Reporte de novedad',
          url: ['/automatizaciones/reporte-novedad'],
        },
        {
          titulo: 'Ejecucion de periodicas',
          url: ['/automatizaciones/ejecucion-periodicas'],
        },
        {
          titulo: "Descargas ID'S",
          url: ['/automatizaciones/descargas-ids'],
        },
      ]
    },  
    
  ];
  
  menuItemsConfiguration = [ 
    { ruta: '/app-picker', icon: 'view_list', tooltip: 'Seleccion de app'},
    { ruta: '/home-configuration', icon: 'home', tooltip: 'Inicio'},
    { ruta: '/configuration/normalizeByAssociate', icon: 'fact_check', tooltip: 'Normalizaciones',
      submenu: [
        //TODO: revisar y quitar los que sean rutas de la aplicacion y ponerlas aqui y las demas revisar a ver para ponerlas
        //en los demas enviroments y mejor utilizar el routeLink para las rutas de la app de cierres las demas si con href si es necesario
        {
          titulo: 'Normalizar por socio',
          url: ['/configuration/normalizeByAssociate'] 
        },
        {
          titulo: 'Mover archivo para reprocesar',
          url: ['/configuration/moveFileReprocess'] 
        },
        {
          titulo: 'Automatizar',
          url: ['/configuration/automate'] 
        }
    ] },
    { ruta: '/configuration/start-pims', icon: 'manage_accounts', tooltip: 'Start Pims' },
    { ruta: '/configuration/generador-bases-emision', icon: 'recent_actors', tooltip: 'Generador Bases de emisión',
      submenu: [
        //TODO: revisar y quitar los que sean rutas de la aplicacion y ponerlas aqui y las demas revisar a ver para ponerlas
        //en los demas enviroments y mejor utilizar el routeLink para las rutas de la app de cierres las demas si con href si es necesario
        {
          titulo: 'Generador bases de emisión',
          url: ['/configuration/generador-bases-emision'] 
        },/*,
        {
          titulo: 'Generador bases de novedades',
          url: ['/configuration/generador-bases-novedades'] 
        }*/
       {
          titulo: 'Registrar Layout',
          url: ['/configuration/register-layout'] 
        },
        {
          titulo: 'Editar Layout',
          url: ['/configuration/edit-layout'] 
        }
    ]
     },

  ];
  menuItemsActuaria = [ 
    { ruta: '/app-picker', icon: 'view_list', tooltip: 'Seleccion de app'},
    { ruta: '/home-actuaria', icon: 'home', tooltip: 'Inicio' },
    { ruta: '/deferred-incentives/update-products', icon: 'calculate', tooltip: 'Incentivos Diferidos' },
    { ruta: '/mes-contable', icon: 'list-alt', tooltip: 'Actualizar mes contable' }    
  ];
  //menu cierres siniestros
  menuItemsCliamsClousing = [
    { ruta: '/app-picker', icon: 'view_list', tooltip: 'Seleccion de app' },
    { ruta: '/home-claims-closing', icon: 'home', tooltip: 'Inicio' },
    /*{ ruta: '/siniestrosWp', icon: 'manage_accounts', tooltip: 'SiniestrosWp',
      submenu: [
        {titulo: 'Radicador', url: '', external: false},
        {titulo: 'Carga Archivo RD', url: '', external: false},
        {titulo: 'Analista', url: '', external: false},
        {titulo: 'Cierre', url: '', external: false},
      ]
     },
    { ruta: '/pagoSiniestros', icon: 'calculate', tooltip: 'Pago de Siniestro',
      submenu: [
        {titulo: 'Análisis', url: '', external: false},
        {titulo: 'Planilla', url: '', external: false},
      ]
     },
    { ruta: '/amdTablas', icon: 'view_stream', tooltip: 'ADM Tablas',
      submenu: [
        {titulo: 'Usuarios', url: '', external: false},
        {titulo: 'Analistas', url: '', external: false},
        {titulo: 'Middle Of.', url: '', external: false},
      ]
     },
    { ruta: '/consultas', icon: 'search', tooltip: 'Consultas',
      submenu: [
        {titulo: 'Estado Cartera', url: '', external: false},
        {titulo: 'Estado Cartera Productos VGD', url: '', external: false},
        {titulo: 'Conf. Cartera Masiva', url: '', external: false},
        {titulo: 'ConsultaSWPDeudores', url: '', external: false}
      ]
     },*/
    { ruta: '/asientosSiniestros', icon: ' fact_check', tooltip: 'Asientos Siniestros',
      submenu: [
        {titulo: 'Reaseguro', url:['/accounting-entry'], external: false},
        {titulo: 'Cardif', url:'', external: false}
      ]
     },
    /*{ ruta: '/cierresAsistencias', icon: 'work_off', tooltip: 'Cierres Asistencias',
      submenu: [
        {titulo: 'Cargue Archivos', url: '', external: false},
        {titulo: 'Dispersar Factura', url: '', external: false},
        {titulo: 'Asientos Contables', url: '', external: false},
        {titulo: 'Reporte por Socio', url: '', external: false}
      ]
     },*/
    { ruta: '/movimientosOnbase', icon: 'account_balance', tooltip: 'Movimientos Onbase Colombia',
      submenu: [ 
        {titulo: 'Cargue Movimientos', url: ['/load-movements-col'], external: false},
        {titulo: 'Reporte Datos', url: ['/report-data-col'], external: false},
        {titulo: 'Reporte Socios', url: ['/partner-report-col'], external: false},
        {titulo: 'Cierre Aval', url: ['/closing-aval'], external: false},
        {titulo: 'Cierre Cardif', url: ['/closing-cardif'], external: false},
        {titulo: 'Homologa Poliza Alfa', url: ['/homologation-policy-alfa'], external: false},
        {titulo: 'Otros Tipos Referencia', url: ['/other-type-reference'], external: false},
        {titulo: 'Reportes Historizados', url: '', external: false},
        {titulo: 'Reaseguro Cuenta Tecnica', url: '', external: false},
        {titulo: 'Novedades Individuales', url: '', external: false}
      ]
    },
    /*{ ruta: '/movimientosCausaciones', icon: 'account_balance', tooltip: 'Movimientos Causaciones',
      submenu: [
        { titulo: 'Cargue Causacion Diaria', url: environment.urlReportingServAuxProd, external: true},
        { titulo: 'Contabiliza Causación', url: environment.urlReportingServAuxProd, external: true},
        { titulo: 'Cargue Pagos Tesoreria', url: environment.urlReportingServAuxProd, external: true},
        { titulo: 'Conciliar Pagos', url: environment.urlReportingServAuxProd, external: true},
        { titulo: 'Auxiliar Pagos', url: environment.urlReportingServAuxProd, external: true}
      ]
     },*/
    { ruta: '/movimientosOnbasePeru', icon: 'account_balance', tooltip: 'Movimientos Onbase Peru',
      submenu: [
        { titulo: 'Cargue Movimientos', url: ['/load-movements-peru'], external: false},
        { titulo: 'Reporte Datos', url: ['/report-data-peru'], external: false},
        { titulo: 'Base Contable', url: ['/peru-accounting-report'], external: false},
        { titulo: 'Ramos', url: ['/ramo-peru'], external: false},
        { titulo: 'Cierre Cardif Peru', url: ['/cardif-peru-closing'], external: false},
        { titulo: 'Cargue Estados', url: environment.urlReportingServAuxProd, external: true}
      ]
     },

    { ruta: '/movimientosCentroamerica', icon: 'account_balance', tooltip: 'Movimientos Centroamerica', 
      submenu: [
        { titulo: 'Cargue Movimientos CA', url: ['/load-movements-ca'], external: false},
        { titulo: 'Reporte Datos CA', url: ['/report-data-ca'], external: false},
        { titulo: 'Cierre Contable CA', url: ['/accounting-closing-ca'], external: false},
        { titulo: 'Reporte Socios CA', url: ['/partner-report-ca'], external: false}
      ]
     },]
     
  menuItemsAcsele = [ 
    { ruta: '/app-picker', icon: 'view_list', tooltip: 'Seleccion de app'},     
    { ruta: '/home-acsele', icon: 'home', tooltip: 'Inicio'},
    {
      ruta: 'reportes-sac', icon: 'person', tooltip: 'Informes PORTAL SAC',
      submenu: [ 
        {
          titulo: 'Eventos Cancelaciones Callcenter',
          url: environment.urlEventosCancelacionesCallcenter,
          external: true,
        },
        {
          titulo: 'Eventos Retenciones Callcenter',
          url: environment.urlEventosRetencionesCallcenter,
          external: true,
        },
        {
          titulo: 'Eventos Retenciones PortalSAC',
          url: environment.urlEventosRetencionesPortalSAC,
          external: true,
        },
        {
          titulo: 'Eventos Retencion CrossSelling',
          url: environment.urlEventosRetencionCrossSelling,
          external: true,
        },
        {
          titulo: 'Cross Selling General Emisiones',
          url: environment.urlCrossSellingGeneralEmisiones,
          external: true,
        },
        {
          titulo: 'Cross Selling General Cancelaciones',
          url: environment.urlCrossSellingGeneralCancelaciones,
          external: true,
        },
        {
          titulo: 'Encripcion De Pagos Banco Popular',
          url: environment.urlEncripcionDePagosBancoPopular,
          external: true,
        },
        {
          titulo: 'No Contactabilidad',
          url: environment.urlNoContactabilidad,
          external: true,
        } 
          ]
        },
  ];
  menuItems = [   ];


  variableRouter: string;

  constructor(
    private router: Router,
    private autenticacionService: AutenticacionService
  ) {
    this.router.events.subscribe(event => {
      this.selectMenu();
      if (event instanceof NavigationEnd) {
        this.rutaActiva = event.urlAfterRedirects;
      }
    });
  }
 
 app: String = null;

 routeEvent(router: string) {
    this.rutaActiva = router; // Guarda la ruta activa
  }

  activarReportes() {
    this.bandReportes =
      this.variableRouter == this.router.url ? !this.bandReportes : false;
    this.routeEvent(this.router.url);
  }

  validarMenu( menu ) {
    return menu.some( obj => obj.ruta === (this.rutaActiva ) 
    || (obj.submenu?.some(sub => sub.url.includes(this.rutaActiva)))  
  );
  }

  activarNovedades() {
    this.bandNovedades =
      this.variableRouter == this.router.url ? !this.bandNovedades : false;
    this.routeEvent(this.router.url);
  }
  ngOnChanges( ) {
    
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.rutaActiva = event.urlAfterRedirects;
      }
    });
    this.selectMenu();
    // changes.prop contains the old and the new value...
  }
  ngOnInit(): void {
    this.selectMenu();
    const usuario = this.autenticacionService.getUserAuthenticate;
    this.routeEvent(this.router.url);
  }

  selectMenu(){ 
    this.app = localStorage.getItem('app');   
    if( this. validarMenu( this.menuItemsConfiguration )  &&  this.rutaActiva  != '/app-picker'  ){ 
      this.menuItems = this.menuItemsConfiguration;      
    }else if( this. validarMenu( this.menuItemsCierres ) &&  this.rutaActiva  != '/app-picker' ){ 
      this.menuItems = this.menuItemsCierres;
    }else if( this. validarMenu( this.menuItemsActuaria )  &&  this.rutaActiva  != '/app-picker' ){ 
      this.menuItems = this.menuItemsActuaria;
    }else if( this. validarMenu( this.menuItemsCliamsClousing )  &&  this.rutaActiva  != '/app-picker' ){ 
      this.menuItems = this.menuItemsCliamsClousing;
    } else if( this. validarMenu( this.menuItemsAcsele )  &&  this.rutaActiva  != '/app-picker' ){ 
      this.menuItems = this.menuItemsAcsele;
    }else{ 
      this.menuItems = [];
    }  
  }

  @HostListener('document:click', ['$event'])
  onClickOutSide(event: MouseEvent) {
    this.selectMenu();
    const clickElement = event.target as HTMLElement;
    const botonElement = document.getElementById('miBoton');
    const botonNovedades = document.getElementById('miBoton1');
    if (botonElement && !botonElement.contains(clickElement)) {
      this.bandReportes = false;
      this.routeEvent(this.router.url);
    } else if (botonNovedades && !botonNovedades.contains(clickElement)) {
      this.bandNovedades = false;
      this.routeEvent(this.router.url);
    }
  }

  enrutamiento(ruta: any) {
    if (ruta == '/reportes') {
    } else {
      this.bandNovedades = false;
      if (ruta == this.router.url) {
        this.bandReportes = false;

        this.routeEvent(ruta);
      } else {
        this.router.navigate([ruta]);
      }
    }
    this.routeEvent(this.router.url);
    this.dropdownActivo = null;
  }

  /**
   * Enrutamiento para ir a la ruta que debe ir el menu.
   */
  goTo(el: any) {
    if (el.external) {
      window.open(el.url, '_blank');
    }
    this.router.navigate(el.url);
    this.dropdownActivo = null;
  }

  toggleDropdown(ruta: string) {
    this.dropdownActivo = this.dropdownActivo === ruta ? null : ruta;
  }
}
