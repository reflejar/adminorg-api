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
      link: "/informes",
      name: "INFORMES",
      icon: <BarChart2 size={18} />
    },    
    {
      link: "/clientes",
      name: "CUENTAS A COBRAR",
      icon: <Download size={18} />
    },
    {
      link: "/proveedores",
      name: "CUENTAS A PAGAR",
      icon: <Upload size={18} />
    },
    {
      link: "/tesoreria",
      name: "TESORERIA",
      icon: <DollarSign size={18} />
    },
    {
      link: "/contabilidad",
      name: "CONTABILIDAD",
      icon: <Briefcase size={18} />
    },
    {
      link: "/comunicacion",
      name: "COMUNICACION",
      icon: <Mail size={18} />
    },
    {
      link: "/configuracion",
      name: "CONFIGURACION",
      icon: <Settings size={18} />
    },
    

  ]

  socio = [
    {
      link: "/deudas",
      name: "MIS DEUDAS",
      icon: <DollarSign size={18} />
    },
    {
      link: "/cuenta",
      name: "MIS MOVIMIENTOS",
      icon: <Layers size={18} />
    },    
    {
      link: "/reportes",
      name: "INFORMES",
      icon: <BarChart2 size={18} />
    },    
    {
      link: "/info",
      name: "MI CUENTA",
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