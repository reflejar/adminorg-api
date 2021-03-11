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
import Spinner from '../../components/spinner/spinner';

// Estructura
import InformesList from "./containers/list";
import InformesSearch from "./containers/search";
import InformesOptions from "./containers/options";

// Contenidos
import FileReader from '../../components/fileReader';
import InfoCarpeta from "../CRUDL/carpeta/CU";
import InfoArchivo from "../CRUDL/archivo/CU";
import TableData from "./tables";

// import CuentaTable from './tables/cuenta';

class Informes extends Component {
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
    const { selected, data, loading } = this.props;
    return (
      <div className="chat-application">
        <div className="content-overlay" />
        <div className="chat-sidebar float-left d-none d-sm-none d-md-block d-lg-block">
          <PerfectScrollbar>
            <div className="chat-sidebar-content">
              <InformesSearch />
              <InformesList selected={selected} />
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
            {loading ? 
              <div className='loading-modal'><Spinner /></div> :
              <TabContent activeTab={this.state.activeTab}>
                <TabPane tabId="1">
                  { data.length > 0 ? <TableData /> : (selected && selected.ubicacion && <FileReader file={selected.ubicacion} />)}
                  {/* { selected ? (selected.ubicacion ? <FileReader file={selected.ubicacion} /> : "Por favor seleccione") : "Que desea realizar?" } */}
                </TabPane>
                <TabPane tabId="2">
                  { selected ? (selected.carpeta ? <InfoArchivo selected={selected} /> : <InfoCarpeta selected={selected} />) : "Por favor seleccione" }
                </TabPane>
            </TabContent>              
            }
          </section>
        </PerfectScrollbar>

        <InformesOptions />
      </div>
    );
  }

}

const mapStateToProps = state => ({
  selected: get(state, 'informes.instance', {}),
  data: get(state, 'informes.data', {}),
  loading: get(state, 'informes.loading')
})

export default connect(mapStateToProps, null)(Informes);