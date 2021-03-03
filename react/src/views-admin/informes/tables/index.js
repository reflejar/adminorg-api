import React, { Component } from "react";
import { connect } from 'react-redux';
import get from 'lodash/get';
import {
   TabContent,
   TabPane,
   Nav,
   NavItem,
   NavLink,
} from "reactstrap";
import classnames from "classnames";
import Operaciones from "./operaciones";
import Sumas from "./sumas";

class TableData extends Component {
   state = {
      activeTab: "1"
   };

   toggle = tab => {
      if (this.state.activeTab !== tab) {
         this.setState({
            activeTab: tab
         });
      }
   };
   render() {
      const {data} = this.props;
      return (
         <div className="tabs-vertical">
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
                    Datos
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
                    Informe
                  </NavLink>
               </NavItem>
               <NavItem>
                  <NavLink
                     className={classnames({
                        active: this.state.activeTab === "3"
                     })}
                     onClick={() => {
                        this.toggle("3");
                     }}
                  >
                    Grafico
                  </NavLink>
               </NavItem>               
            </Nav>
            <TabContent activeTab={this.state.activeTab}>
               <TabPane tabId="1">
                  <Operaciones data={data}/>
               </TabPane>
               <TabPane tabId="2">
                  <Sumas />
               </TabPane>
               <TabPane tabId="3">
                  Aqui
               </TabPane>
            </TabContent>
         </div>
      );
   }
}

const mapStateToProps = state => ({
   data: get(state, 'informes.data', {}),
}) 
 
export default connect(mapStateToProps, null)(TableData);