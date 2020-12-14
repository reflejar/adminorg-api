import React, { useState, Fragment } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import {
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";
import { connect } from 'react-redux'
import get from 'lodash/get';
import { Modal, ModalHeader, ModalBody, Button } from "reactstrap";

// Estructura
import List from "./containers/list";
import Options from '../../components/board/options';

import Clientes from "./containers/tablas/clientes";
import Dominios from "./containers/tablas/dominios";
import Proveedores from "./containers/tablas/proveedores";
import Cajas from "./containers/tablas/cajas";
import Ingresos from "./containers/tablas/ingresos";
import Gastos from "./containers/tablas/gastos";
import Intereses from "./containers/tablas/intereses";
import Descuentos from "./containers/tablas/descuentos";

import Cliente from "../CRUDL/cliente/CU";
import ClienteMasivo from "../CRUDL/cliente/M";
import Dominio from "../CRUDL/dominio/CU";
import DominioMasivo from "../CRUDL/dominio/M";
import Proveedor from "../CRUDL/proveedor/CU";
import ProveedorMasivo from "../CRUDL/proveedor/M";
import Caja from "../CRUDL/caja/CU";
import CajaMasivo from "../CRUDL/caja/M";
import Ingreso from "../CRUDL/ingreso/CU";
import IngresoMasivo from "../CRUDL/ingreso/M";
import Gasto from "../CRUDL/gasto/CU";
import GastoMasivo from "../CRUDL/gasto/M";
import Interes from "../CRUDL/interes/CU";
import Descuento from "../CRUDL/descuento/CU";


const Configuraciones = ({selected}) => {

  const [modal, setModal] = useState(false)
  const [item, setItem] = useState(null)
  const [method, setMethod] = useState("individual")
  
  const toggle = (method) => {
    setItem(null);
    setModal(!modal);
    setMethod(method)
  }

  const tables = {
    cliente: <Clientes toggle={setModal} setItem={setItem} />,
    dominio: <Dominios toggle={setModal} setItem={setItem} />,
    proveedor: <Proveedores toggle={setModal} setItem={setItem} />,
    caja: <Cajas toggle={setModal} setItem={setItem} />,
    ingreso: <Ingresos toggle={setModal} setItem={setItem} />,
    gasto: <Gastos toggle={setModal} setItem={setItem} />,
    interes: <Intereses toggle={setModal} setItem={setItem} />,
    descuento: <Descuentos toggle={setModal} setItem={setItem} />,
  }


  const modals = (editItem) => ({
      cliente: {
        individual: <Cliente onClose={setModal} selected={editItem ? item : null} />,
        masivo: <ClienteMasivo onClose={() => toggle("masivo")} />
      },
      dominio: {
        individual: <Dominio onClose={setModal} selected={editItem ? item : null} />,
        masivo: <DominioMasivo onClose={() => toggle("masivo")} />
      },
      proveedor: {
        individual: <Proveedor onClose={setModal} selected={editItem ? item : null} />,
        masivo: <ProveedorMasivo onClose={() => toggle("masivo")} />
      },
      caja: {
        individual: <Caja onClose={setModal} selected={editItem ? item : null} />,
        masivo: <CajaMasivo onClose={() => toggle("masivo")} />
      },
      ingreso: {
        individual: <Ingreso onClose={setModal} selected={editItem ? item : null} />,
        masivo: <IngresoMasivo onClose={() => toggle("masivo")} />
      },
      gasto: {
        individual: <Gasto onClose={setModal} selected={editItem ? item : null} />,
        masivo: <GastoMasivo onClose={() => toggle("masivo")} />
      },
      interes: {
        individual: <Interes onClose={setModal} selected={editItem ? item : null} />,
        masivo: "No es posible realizar importacion de las metodologias de intereses"
      },
      descuento: {
        individual: <Descuento onClose={setModal} selected={editItem ? item : null} />,
        masivo: "No es posible realizar importacion de las metodologias de descuento"
      },
    })
  
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
        toggle={() => toggle(method)}
        backdrop="static"
      >
  
      <ModalHeader toggle={() => toggle(method)}>{item ? "Editar" : "Nuevo"}</ModalHeader>
      <ModalBody>
        { item ? modals(true)[item.causante]['individual'] : selected && modals(false)[selected.id][method] }
      </ModalBody>
      
    </Modal>    


    <PerfectScrollbar>
      <section className="chat-app-window">
        { selected ? tables[selected.id] : "Por favor seleccione" }
      </section>
    </PerfectScrollbar>

    <Options
      leftOps={[
        <Button disabled={!selected} outline onClick={() => toggle("individual")} color="primary">Nuevo</Button>,
        <Button disabled={!selected} outline onClick={() => toggle("masivo")} color="primary">Importar</Button>,
      ]}
      rightOps={[]}        
    />

    </div>
  </Fragment>    
  )
}

const mapStateToProps = state => ({
  selected: get(state, 'configuraciones.instance', {}),
})

export default connect(mapStateToProps, null)(Configuraciones);