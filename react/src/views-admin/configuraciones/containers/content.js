import { connect } from "react-redux";
import React, { Component, Fragment } from "react";

import Clientes from "../../tablas/clientes";
import Dominios from "../../tablas/dominios";
import Proveedores from "../../tablas/proveedores";
import Ingresos from "../../tablas/ingresos";
import Gastos from "../../tablas/gastos";
import Cajas from "../../tablas/cajas";
import Intereses from "../../tablas/intereses";
import Descuentos from "../../tablas/descuentos";

const tables = {
  cliente: <Clientes />,
  dominio: <Dominios />, 
  proveedor: <Proveedores />,
  ingreso: <Ingresos />,
  gasto: <Gastos />,
  caja: <Cajas />,
  interes: <Intereses />,
  descuento: <Descuentos />,
  
}


class Content extends Component {

    render() {
      const { item } = this.props;
      let body = ""
      if (item) {
        body = tables[item.id]
      }

      return (
          <Fragment>
              {body}
          </Fragment>
      )
    }

  }

const mapStateToProps = state => ({
  item: state.configuraciones.list.find(i => i.id === state.configuraciones.instance)
})

export default connect(
  mapStateToProps,
)(Content);