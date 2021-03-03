import { combineReducers } from "redux";

import customizer from "./customizer/";
import { reducer as toastrReducer } from "react-redux-toastr";

import clientes from './clientes';
import dominios from './dominios';
import proveedores from './proveedores';
import ingresos from './ingresos';
import gastos from './gastos';
import cajas from './cajas';
import intereses from './intereses';
import descuentos from './descuentos';
import configuraciones from './configuraciones';
import contabilidad from './contabilidad';
import user from './user';
import utils from './utils'; // Eliminar esto
import titulos from './titulos';
import puntos from './puntos';
import deudas from './deudas';
import cuentas from './cuentas';
import preconceptos from './preconceptos';
import documentos from './documentos';
import plataforma from './plataforma';
import saldos from './saldos';
import retenciones from './retenciones';
import informes from './informes';
import carpetas from './carpetas';

const appReducer = combineReducers({
   toastr: toastrReducer, // <- Mounted at toastr.
   customizer,
   clientes,
   carpetas,
   dominios,
   informes,
   proveedores,
   ingresos,
   gastos,
   cajas,
   intereses,
   descuentos,
   contabilidad,
   configuraciones,
   user,
   utils, //Eliminar esto
   titulos,
   puntos,
   deudas,
   cuentas,
   preconceptos,
   documentos,
   plataforma,
   saldos,
   retenciones
});

const rootReducer = (state, action) => {
   if (action.type === "LOGOUT") {
      localStorage.clear();
      state = undefined;
   }

   return appReducer(state, action);
}

export default rootReducer;
