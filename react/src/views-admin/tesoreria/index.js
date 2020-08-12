import React, { Component } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import {
  Nav,
  NavItem,
  NavLink,
  TabContent,
  TabPane,
} from "reactstrap";
import classnames from "classnames";
import { connect } from 'react-redux'
import get from 'lodash/get';

// Estructura
import CajaList from "./containers/list";
import CajaSearch from "./containers/search";
import CajaOptions from "./containers/options";

// Contenidos
import Deudas from '../../components/board/content/deudas';
import Cuenta from '../../components/board/content/cuenta';
import Info from "../CRUDL/caja/CU";

import StockTable from './tables/stock';
import CuentaTable from './tables/cuenta';

class Tesoreria extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: "1"
    };
  }

  toggle(tab) {
    if (this.state.activeTab !== tab) {
      this.setState({
        activeTab: tab
      });
    }
  }

  render() {
    const { selected } = this.props;
    return (
      <div className="chat-application">
        <div className="content-overlay" />
        <div className="chat-sidebar float-left d-none d-sm-none d-md-block d-lg-block">
          <PerfectScrollbar>
            <div className="chat-sidebar-content">
              <CajaSearch />
              <CajaList />
            </div>
          </PerfectScrollbar>
        </div>

        <div className="chat-name no-border p-1 bg-white">
          <Nav tabs>
            <NavItem>
              <NavLink
                className={classnames({
                  active: this.state.activeTab === "1"
                })}
                onClick={() => {
                  this.toggle("1");
                }}
              >
                Movimientos
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                className={classnames({
                  active: this.state.activeTab === "2"
                })}
                onClick={() => {
                  this.toggle("2");
                }}
              >
                Stock de disponibilidades
              </NavLink>
            </NavItem>            
            <NavItem>
              <NavLink
                className={classnames({
                  active: this.state.activeTab === "3"
                })}
                onClick={() => {
                  this.toggle("3");
                }}>
                Informacion
              </NavLink>
            </NavItem>
          </Nav>
        </div>

        <PerfectScrollbar>
          <section className="chat-app-window">
            <TabContent activeTab={this.state.activeTab}>
              <TabPane tabId="1">
                { selected ? <Cuenta selected={selected} Table={CuentaTable} /> : "Por favor seleccione" }
              </TabPane>
              <TabPane tabId="2">
                { selected ? <Deudas selected={selected} Table={StockTable}/> : "Por favor seleccione" }
              </TabPane>              
              <TabPane tabId="3">
                { selected ? <Info selected={selected} /> : "Por favor seleccione" }
              </TabPane>
            </TabContent>
          </section>
        </PerfectScrollbar>

        <CajaOptions />
      </div>
    );
  }

}

const mapStateToProps = state => ({
  selected: get(state, 'cajas.instance', {}),
})

export default connect(mapStateToProps, null)(Tesoreria);