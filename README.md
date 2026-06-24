app-routing.module.ts

import { CardifPeruClosingComponent } from './views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component';

{ path: 'cardif-peru-closing', component: CardifPeruClosingComponent, canActivate: [AuthenticateGuardian], data: { menuKey: 'ClaimsClosing', } },


nav-bar.component.ts

{ titulo: 'Cierre Cardif Peru', url: ['/cardif-peru-closing'], external: false},

