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
import UtilizacionesSaldos from "./utilizacionesSaldos";
import Retenciones from "./retenciones";

import './styles.scss'

import { useSaldos, useCajas, useRetenciones } from '../../../../utility/hooks/dispatchers';


const FormasPago = ({ documento, setDocumento, destinatario, errors, update }) => {

  const [tesoros, loadingTesoros] = useCajas();
  const [saldos, loadingSaldos] = useSaldos(false, destinatario);
  const [retenciones, loadingRetenciones] = useRetenciones();

  
  const insertBadge = (data) => {
    if (data && data.length > 0) {
      return <Badge pill color="success">{data.length}</Badge>
    }
  }

  const activeTabInitial = () => {
    if (update && documento.cajas && documento.utilizaciones_saldos && documento.retenciones) {
      const formaMayor = [{
        campo: "1",
        cantidad: documento.cajas.length 
      }, {
        campo: "2",
        cantidad: documento.utilizaciones_saldos.length 
      }, {
        campo: "3",
        cantidad: documento.retenciones.length 
      },
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
        <h3 className="pl-0 credito__row__header__text">Formas de pago</h3>
        {loadingSaldos || loadingRetenciones || loadingTesoros ?
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
                  Tesoreria {update && insertBadge(documento.cajas)}
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink
                  disabled={update ? (get(documento, 'utilizaciones_saldos', []).length === 0 && true) : (documento.pagos && documento.pagos.length === 0) ? true : false}
                  className={classnames({
                      active: activeTab === "2"
                  })}
                  onClick={() => {
                      toggle("2");
                  }}
                >
                  {update ? "Utilizaciones de": "Utilizar"} Saldos anteriores {update ? insertBadge(documento.utilizaciones_saldos) : insertBadge(saldos)}
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink
                  disabled={update && get(documento, 'retenciones', []).length === 0 && true}
                  className={classnames({
                    active: activeTab === "3"
                  })}
                  onClick={() => {
                    toggle("3");
                  }}
                  >
                  Retenciones {update ? insertBadge(documento.retenciones) : ""}
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
                    <UtilizacionesSaldos
                      documento={documento} 
                      setDocumento={setDocumento}
                      saldos={saldos}
                      errors={errors} 
                      update={update}/>
                  </Col>
                </Row>
            </TabPane>
            <TabPane tabId="3">
                <Row>
                  <Col sm="12">
                    <Retenciones
                      documento={documento} 
                      setDocumento={setDocumento}
                      retenciones={retenciones}
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