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
import ContabilidadList from "./containers/list";
import ContabilidadSearch from "./containers/search";
import ContabilidadOptions from "./containers/options";

// Contenidos
import Cuenta from '../../components/board/content/cuenta';
// import Info from "../CRUDL/contabilidad/CU";

import CuentaTable from './tables/cuenta';

class Contabilidad extends Component {
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
        <div className="chat2-sidebar float-left d-none d-sm-none d-md-block d-lg-block">
          <PerfectScrollbar>
            <div className="chat2-sidebar-content">
              <ContabilidadSearch />
              <ContabilidadList selected={selected} />
            </div>
          </PerfectScrollbar>
        </div>

        <div className="chat2-name no-border p-1 bg-white">
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
                Cuenta historica
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                className={classnames({
                  active: this.state.activeTab === "2"
                })}
                onClick={() => {
                  this.toggle("2");
                }}>
                Informacion del titulo
              </NavLink>
            </NavItem>
          </Nav>
        </div>

        <PerfectScrollbar>
          <section className="chat2-app-window">
            <TabContent activeTab={this.state.activeTab}>
              <TabPane tabId="1">
                { selected ? <Cuenta selected={selected} Table={CuentaTable} /> : "Por favor seleccione" }
              </TabPane>
              <TabPane tabId="2">
                {/* { selected ? <Info selected={selected} /> : "Por favor seleccione" } */}
              </TabPane>
            </TabContent>
          </section>
        </PerfectScrollbar>

        <ContabilidadOptions />
      </div>
    );
  }

}

const mapStateToProps = state => ({
  selected: get(state, 'contabilidad.instance', {}),
})

export default connect(mapStateToProps, null)(Contabilidad);