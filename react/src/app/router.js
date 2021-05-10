// import external modules
import React, { Component, Suspense, lazy } from "react";
import { BrowserRouter, Switch } from "react-router-dom";
import Spinner from "../components/spinner/spinner";

// import internal(own) modules
import LandingLayoutRoute from "../layouts/routes/landingRoutes";
import MainLayoutRoute from "../layouts/routes/mainRoutes";
import FullPageLayoutRoute from "../layouts/routes/fullpageRoutes";
import ErrorLayoutRoute from "../layouts/routes/errorRoutes";

// Rutas publicas (Tienen Layout completo)
const LazyLanding = lazy(() => import("../views/landing"));
const LazyLogin = lazy(() => import("../views/auth/login"));
const LazyForgotPassword = lazy(() => import("../views/auth/forgotPassword"));
const LazyRegister = lazy(() => import("../views/auth/register"));

// Rutas privadas (Tienen Dashboard)
const LazyUserProfile = lazy(() => import("../views/user"));
const LazyFAQ = lazy(() => import("../views/faq"));
const LazyClientes = lazy(() => import("../views-admin/clientes"));
const LazyProveedores = lazy(() => import("../views-admin/proveedores"));
const LazyTesoreria = lazy(() => import("../views-admin/tesoreria"));
const LazyContabilidad = lazy(() => import("../views-admin/contabilidad"));
const LazyInformes = lazy(() => import("../views-admin/informes"));
const LazyComunicacion = lazy(() => import("../views/comunicacion"));
const LazyConfiguracion = lazy(() => import("../views-admin/configuraciones"));
const LazyDeudas = lazy(() => import("../views-socio/deudas"));
const LazyCuenta = lazy(() => import("../views-socio/cuenta"));
const LazyReportes = lazy(() => import("../views-socio/reportes"));

// Error Pages
const LazyErrorPage = lazy(() => import("../views/errors"));

class Router extends Component {
   render() {
      return (
         // Set the directory path if you are deplying in sub-folder
         <BrowserRouter basename="/">
            <Switch>
               {/* Rutas publicas */}
               <LandingLayoutRoute
                  exact
                  path="/"
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyLanding {...matchprops} />
                     </Suspense>
                  )}
               />               
               <FullPageLayoutRoute
                  exact
                  path="/login"
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyLogin {...matchprops} />
                     </Suspense>
                  )}
               />

               {/* Rutas privadas */}

               <MainLayoutRoute
                  exact
                  path="/clientes"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyClientes {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/proveedores"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyProveedores {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/tesoreria"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyTesoreria {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/contabilidad"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyContabilidad {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/informes"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyInformes {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/configuracion"
                  groups={['administrativo']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyConfiguracion {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/deudas"
                  groups={['socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyDeudas {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/cuenta"
                  groups={['socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyCuenta {...matchprops} />
                     </Suspense>
                  )}
               />                   
               <MainLayoutRoute
                  exact
                  path="/reportes"
                  groups={['socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyReportes {...matchprops} />
                     </Suspense>
                  )}
               />


               {/* Joint Pages Views */}
               <MainLayoutRoute
                  exact
                  path="/comunicacion"
                  groups={['administrativo', 'socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyComunicacion {...matchprops} />
                     </Suspense>
                  )}
               />                                     
               <MainLayoutRoute
                  exact
                  path="/faq"
                  groups={['administrativo', 'socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyFAQ {...matchprops} />
                     </Suspense>
                  )}
               />
               <MainLayoutRoute
                  exact
                  path="/user-profile"
                  groups={['administrativo', 'socio']}
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyUserProfile {...matchprops} />
                     </Suspense>
                  )}
               />


               {/* Saperate Pages Views */}
               <FullPageLayoutRoute
                  exact
                  path="/forgot-password"
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyForgotPassword {...matchprops} />
                     </Suspense>
                  )}
               />
               <FullPageLayoutRoute
                  exact
                  path="/login"
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyLogin {...matchprops} />
                     </Suspense>
                  )}
               />
               <FullPageLayoutRoute
                  exact
                  path="/register"
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyRegister {...matchprops} />
                     </Suspense>
                  )}
               />



               <ErrorLayoutRoute
                  render={matchprops => (
                     <Suspense fallback={<Spinner />}>
                        <LazyErrorPage {...matchprops} />
                     </Suspense>
                  )}
               />
            </Switch>
         </BrowserRouter>
      );
   }
}

export default Router;
