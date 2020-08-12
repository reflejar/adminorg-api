import React from "react";
import { Route, Redirect } from "react-router-dom";
import { connect } from 'react-redux';

import MainLayout from "../mainLayout";

const MainLayoutRoute = ({ groups, render, ...rest }) => {
   
   const currentUser = rest.currentUser;

   return (
      <Route
         {...rest}
         render={matchProps => {
            if (!currentUser) {
               return <Redirect to={{ pathname: '/login', state: { from: matchProps.location } }} />
            }
            if (groups && groups.indexOf(currentUser.user.group) === -1){
               return <Redirect to={{ pathname: '/login', state: { from: matchProps.location } }} />
            }
            return <MainLayout>{render(matchProps)}</MainLayout> 
         }}
      />
   );
};

const mapStateToProps = (state) => ({
   currentUser: state.user.auth,
});

export default connect(mapStateToProps, null)(MainLayoutRoute);