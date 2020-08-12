import React, { useState } from 'react';
import get from 'lodash/get';
import {
   TabContent,
   TabPane,
   Nav,
   NavItem,
   NavLink,
   Row,
   Col,
   Badge
  } from "reactstrap";
import classnames from "classnames";
import Spinner from '../../../../components/spinner/spinner';

// Contenido
import Cajas from "./cajaNew";
import UtilizacionesDisponibilidades from "./utilizacionesDisponibilidades";

import './styles.scss'

import { useCajas, useDisponibilidades } from '../../../../utility/hooks/dispatchers';


const FormasPago = ({ documento, setDocumento, errors, update }) => {

  const [tesoros, loadingTesoros] = useCajas();
  const [disponibilidades, loadingDisponibilidades] = useDisponibilidades();

  
  const insertBadge = (data) => {
    if (data && data.length > 0) {
      return <Badge pill color="success">{data.length}</Badge>
    }
  }

  const activeTabInitial = () => {
    if (update && documento.cajas && documento.utilizaciones_disponibilidades) {
      const formaMayor = [{
        campo: "1",
        cantidad: documento.cajas.length 
      }, {
        campo: "2",
        cantidad: documento.utilizaciones_disponibilidades.length 
      }
    ].sort((a, b) => (a.cantidad > b.cantidad) ? -1 : 1)
      return formaMayor[0].campo
    }

    return "1"
  }
  

  const [activeTab, setActiveTab] = useState(activeTabInitial());

  const toggle = tab => {
    if (activeTab !== tab) {
     setActiveTab(tab);
    }
  };

  

  return (
    <Row>
      <Col sm="12">
        <h3 className="pl-0 credito__row__header__text">Descargas a generar</h3>
        {loadingDisponibilidades || loadingTesoros ?
          <div className='loading-modal'>
            <Spinner />
          </div> :
        <div className="FormasPago">
        <div className="">
          <Nav tabs>
            <NavItem>
                <NavLink
                  disabled={update && get(documento, 'cajas', []).length === 0 && true}
                  className={classnames({
                      active: activeTab === "1"
                  })}
                  onClick={() => {
                      toggle("1");
                  }}
                >
                  Descargas {update ? "creadas": "nuevas"} {update && insertBadge(documento.cajas)}
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink
                  disabled={update ? (get(documento, 'utilizaciones_disponibilidades', []).length === 0 && true) : (documento.pagos && documento.pagos.length === 0) ? true : false}
                  className={classnames({
                      active: activeTab === "2"
                  })}
                  onClick={() => {
                      toggle("2");
                  }}
                >
                  {update ? "Descargas de": "Descargar"} Disponibilidades 
                </NavLink>
            </NavItem>           
          </Nav>
        </div>
        <div className="FormasPago__body">
          <TabContent activeTab={activeTab}>
            <TabPane tabId="1">
                <Row>
                  <Col sm="12">
                    <Cajas
                      documento={documento} 
                      setDocumento={setDocumento} 
                      tesoros={tesoros}
                      errors={errors} 
                      update={update}/>
                  </Col>
                </Row>            
            </TabPane>
            <TabPane tabId="2">
                <Row>
                  <Col sm="12">
                    <UtilizacionesDisponibilidades
                      documento={documento} 
                      setDocumento={setDocumento}
                      disponibilidades={disponibilidades}
                      errors={errors} 
                      update={update}/>
                  </Col>
                </Row>
            </TabPane>         
          </TabContent>
        </div>
      </div>          
      }

      </Col>
    </Row>
  );
};


export default FormasPago;