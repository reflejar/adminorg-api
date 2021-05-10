import React from 'react';
import Header from './components/landing/Header';
import Footer from './components/landing/Footer';
import classnames from "classnames";

const LayoutPageDefault = ({ children }) => (
  <>
     <div
        className={classnames("login-layout wrapper ", {
           "layout-dark": true
        })}
     >  
      <Header navPosition="right" className="reveal-from-bottom" />
      <main className="site-content">
        {children}
      </main>
      <Footer />
    </div>    
  </>
);

export default LayoutPageDefault;  
