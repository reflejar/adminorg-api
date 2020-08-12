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
import UtilizacionesDisponibilidades from "./utilizacionesDisponibilidades";

import './styles.scss'

import { useSaldos, useCajas, useDisponibilidades } from '../../../../utility/hooks/dispatchers';


const FormasCobro = ({ documento, setDocumento, destinatario, errors, onlyRead }) => {

  const [tesoros, loadingTesoros] = useCajas();
  const [saldos, loadingSaldos] = useSaldos(false, destinatario);
  const [disponibilidades, loadingDisponibilidades] = useDisponibilidades();

  
  const insertBadge = (data) => {
    if (data && data.length > 0) {
      return <Badge pill color="success">{data.length}</Badge>
    }
  }

  const activeTabInitial = () => {
    if (onlyRead && documento.cajas && documento.utilizaciones_saldos && documento.utilizaciones_disponibilidades) {
      const formaMayor = [{
        campo: "1",
        cantidad: documento.cajas.length 
      }, {
        campo: "2",
        cantidad: documento.utilizaciones_saldos.length 
      }, {
        campo: "3",
        cantidad: documento.utilizaciones_disponibilidades.length 
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
        <h3 className="pl-0 credito__row__header__text">Formas de cobro</h3>
        {loadingSaldos || loadingDisponibilidades || loadingTesoros ?
          <div className='loading-modal'>
            <Spinner />
          </div> :
        <div className="FormasCobro">
        <div className="">
          <Nav tabs>
            <NavItem>
                <NavLink
                  disabled={onlyRead && get(documento, 'cajas', []).length === 0 && true}
                  className={classnames({
                      active: activeTab === "1"
                  })}
                  onClick={() => {
                      toggle("1");
                  }}
                >
                  Tesoreria {onlyRead && insertBadge(documento.cajas)}
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink
                  disabled={onlyRead ? (get(documento, 'utilizaciones_saldos', []).length === 0 && true) : (documento.cobros && documento.cobros.length === 0 && true)}
                  className={classnames({
                      active: activeTab === "2"
                  })}
                  onClick={() => {
                      toggle("2");
                  }}
                >
                  {onlyRead ? "Utilizaciones de": "Utilizar"} Saldos anteriores {onlyRead ? insertBadge(documento.utilizaciones_saldos) : insertBadge(saldos)}
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink
                  disabled={onlyRead && get(documento, 'utilizaciones_disponibilidades', []).length === 0 && true}
                  className={classnames({
                    active: activeTab === "3"
                  })}
                  onClick={() => {
                    toggle("3");
                  }}
                  >
                  {onlyRead ? "Utilizaciones de": "Utilizar"} Disponibilidades
                </NavLink>
            </NavItem>             
          </Nav>
        </div>
        <div className="FormasCobro__body">
          <TabContent activeTab={activeTab}>
            <TabPane tabId="1">
                <Row>
                  <Col sm="12">
                    <Cajas
                      documento={documento} 
                      setDocumento={setDocumento} 
                      tesoros={tesoros}
                      errors={errors} 
                      onlyRead={onlyRead}/>
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
                      onlyRead={onlyRead}/>
                  </Col>
                </Row>
            </TabPane>
            <TabPane tabId="3">
                <Row>
                  <Col sm="12">
                    <UtilizacionesDisponibilidades
                      documento={documento} 
                      setDocumento={setDocumento}
                      disponibilidades={disponibilidades}
                      errors={errors} 
                      onlyRead={onlyRead}/>
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


export default FormasCobro;