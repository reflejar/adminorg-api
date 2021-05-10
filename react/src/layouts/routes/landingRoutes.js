// import external modules
import React , { useRef, useEffect } from "react";
import { Route, Switch, useLocation } from "react-router-dom";
import ScrollReveal from './utils/ScrollReveal';

// import internal(own) modules
import LayoutPageDefault from "../landingPageLayout";

const LandingPageLayoutRoute = ({ render, ...rest }) => {


   const childRef = useRef();
   let location = useLocation();
 
   useEffect(() => {
     document.body.classList.add('is-loaded')
     childRef.current.init();
     // eslint-disable-next-line react-hooks/exhaustive-deps
   }, [location]);
 
   return (
      <ScrollReveal
        ref={childRef}
        children={() => (
          <Switch>
            <Route
               {...rest}
               render={matchProps => {
                  return <LayoutPageDefault>{render(matchProps)}</LayoutPageDefault>
               }}
            />             
          </Switch>
        )} />
    );   

};
export default LandingPageLayoutRoute;