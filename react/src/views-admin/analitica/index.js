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
import AnaliticaList from "./containers/list";
import AnaliticaSearch from "./containers/search";
import AnaliticaOptions from "./containers/options";

// Contenidos
// import Cuenta from '../../components/board/content/cuenta';
import InfoCarpeta from "../CRUDL/carpeta/CU";
import InfoArchivo from "../CRUDL/carpeta/CU";

// import CuentaTable from './tables/cuenta';

class Analitica extends Component {
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
              <AnaliticaSearch />
              <AnaliticaList selected={selected} />
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
                Reporte
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
                Detalles
              </NavLink>
            </NavItem>
          </Nav>
        </div>

        <PerfectScrollbar>
          <section className="chat-app-window">
            <TabContent activeTab={this.state.activeTab}>
              <TabPane tabId="1">
                {/* { selected ? <Cuenta selected={selected} Table={CuentaTable} /> : "Por favor seleccione" } */}
              </TabPane>
              <TabPane tabId="2">
                { selected ? (selected.supercarpeta ? <InfoCarpeta selected={selected} /> : <InfoArchivo selected={selected} />) : "Por favor seleccione" }
              </TabPane>
            </TabContent>
          </section>
        </PerfectScrollbar>

        <AnaliticaOptions />
      </div>
    );
  }

}

const mapStateToProps = state => ({
  selected: get(state, 'analitica.instance', {}),
})

export default connect(mapStateToProps, null)(Analitica);