// import external modules
import React, { Component } from "react";

import {
  Download,
  Upload,
  Mail,
  Briefcase,
  Settings,
  BarChart2,
  DollarSign,
  Layers,
  User
} from "react-feather";
import { NavLink } from "react-router-dom";
import { connect } from 'react-redux';

// Styling
import "../../../../assets/scss/components/sidebar/sidemenu/sidemenu.scss";
// import internal(own) modules
import SideMenu from "../sidemenuHelper";

class SideMenuContent extends Component {

  administrativo = [ 
    {
      link: "/analitica",
      name: "Analitica",
      icon: <BarChart2 size={18} />
    },    
    {
      link: "/clientes",
      name: "Cuentas a cobrar",
      icon: <Download size={18} />
    },
    {
      link: "/proveedores",
      name: "Cuentas a pagar",
      icon: <Upload size={18} />
    },
    {
      link: "/tesoreria",
      name: "Tesoreria",
      icon: <DollarSign size={18} />
    },
    {
      link: "/contabilidad",
      name: "Contabilidad",
      icon: <Briefcase size={18} />
    },
    {
      link: "/comunicacion",
      name: "Comunicacion",
      icon: <Mail size={18} />
    },
    {
      link: "/configuracion",
      name: "Configuracion",
      icon: <Settings size={18} />
    },
    

  ]

  socio = [
    {
      link: "/deudas",
      name: "Estado de Deudas",
      icon: <DollarSign size={18} />
    },
    {
      link: "/cuenta",
      name: "Estado de Cuenta",
      icon: <Layers size={18} />
    },    
    {
      link: "/reportes",
      name: "Reportes",
      icon: <Briefcase size={18} />
    },    
    {
      link: "/comunicacion",
      name: "Comunicacion",
      icon: <Mail size={18} />
    },    
    {
      link: "/info",
      name: "Info de Cuenta",
      icon: <User size={18} />
    },        
  ]

  group = () => {
    const { currentGroup } = this.props 
    if (currentGroup === "administrativo") {
      return this.administrativo
    } else {
      return this.socio
    }
  }
  
  render() {  
      return (
         <SideMenu className="sidebar-content" toggleSidebarMenu={this.props.toggleSidebarMenu}>

          {this.group().map((obj, i) => (
          <SideMenu.MenuSingleItem key={i}>
            <NavLink to={obj.link}  activeClassName="active">
              <i className="menu-icon">
                {obj.icon}
              </i>
              <span className="menu-item-text">{obj.name}</span>
            </NavLink>
          </SideMenu.MenuSingleItem>
          ))}
     
         </SideMenu>
      );
   }
}

const mapStateToProps = (state) => ({
  currentGroup: state.user.auth.user.group,
});

export default connect(mapStateToProps, null)(SideMenuContent);