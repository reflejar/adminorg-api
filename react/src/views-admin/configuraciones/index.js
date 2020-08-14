import React, { useState, Fragment } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import {
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";
import { connect } from 'react-redux'
import get from 'lodash/get';
import { Modal, ModalHeader, ModalBody } from "reactstrap";

// Estructura
import List from "./containers/list";
import Options from "./containers/options";

import Clientes from "./containers/tablas/clientes";
import Dominios from "./containers/tablas/dominios";
import Proveedores from "./containers/tablas/proveedores";
import Cajas from "./containers/tablas/cajas";
import Ingresos from "./containers/tablas/ingresos";
import Gastos from "./containers/tablas/gastos";
import Intereses from "./containers/tablas/intereses";
import Descuentos from "./containers/tablas/descuentos";

import Cliente from "../CRUDL/cliente/CU";
import Dominio from "../CRUDL/dominio/CU";
import Proveedor from "../CRUDL/proveedor/CU";
import Caja from "../CRUDL/caja/CU";
import Ingreso from "../CRUDL/ingreso/CU";
import Gasto from "../CRUDL/gasto/CU";
import Interese from "../CRUDL/dominio/CU";
import Descuento from "../CRUDL/dominio/CU";


const Configuraciones = ({selected}) => {

  const [modal, setModal] = useState(false)
  const [item, setItem] = useState({})
  
  const toggle = () => setModal(!modal);

  const tables = {
    cliente: <Clientes toggle={toggle} setItem={setItem} />,
    dominio: <Dominios toggle={toggle} setItem={setItem} />,
    proveedor: <Proveedores toggle={toggle} setItem={setItem} />,
    caja: <Cajas toggle={toggle} setItem={setItem} />,
    ingreso: <Ingresos toggle={toggle} setItem={setItem} />,
    gasto: <Gastos toggle={toggle} setItem={setItem} />,
    interes: <Intereses toggle={toggle} setItem={setItem} />,
    descuento: <Descuentos toggle={toggle} setItem={setItem} />,
  }

  const edit = {
    cliente: <Cliente onClose={toggle} selected={item} />,
    dominio: <Dominio onClose={toggle} selected={item} />,
    proveedor: <Proveedor onClose={toggle} selected={item} />,
    caja: <Caja onClose={toggle} selected={item} />,
    ingreso: <Ingreso onClose={toggle} selected={item} />,
    gasto: <Gasto onClose={toggle} selected={item} />,
    interes: <Interese onClose={toggle} selected={item} />,
    descuento: <Descuento onClose={toggle} selected={item} />,
  }
  
  return (
    <Fragment>
    <div className="chat-application">
      <div className="content-overlay"></div>
      <div className="chat-sidebar float-left d-none d-sm-none d-md-block d-lg-block">
        <div className="chat-sidebar-content">
          <List />
        </div>
      </div>

      <div className="chat-name no-border p-1 bg-white">
      <Nav tabs>
        <NavItem>
          <NavLink className="active">
            Listado
          </NavLink>
        </NavItem>
      </Nav>
    </div>

    <Modal
        isOpen={modal}
        size="xl"
        toggle={toggle}
        backdrop="static"
      >
  
      <ModalHeader toggle={toggle}>Editar</ModalHeader>
  
      <ModalBody>
        { item && edit[item.causante] }
      </ModalBody>
      
    </Modal>    


    <PerfectScrollbar>
      <section className="chat-app-window">
        { selected ? tables[selected.id] : "Por favor seleccione" }
      </section>
    </PerfectScrollbar>

    <Options edit={edit} />
    
    </div>
  </Fragment>    
  )
}

const mapStateToProps = state => ({
  selected: get(state, 'configuraciones.instance', {}),
})

export default connect(mapStateToProps, null)(Configuraciones);