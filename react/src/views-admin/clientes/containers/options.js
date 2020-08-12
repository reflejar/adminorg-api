import React, { Component } from "react";
import { connect } from 'react-redux';

import Options from '../../../components/board/options';
import ModalFactura from '../modals/factura';
import ModalNotaCredito from '../modals/nota-credito';
import ModalCobro from "../modals/recibo-x";
import ModalFacturacionMasiva from "../modals/factura-masiva";
import ModalPreconceptos from "../modals/preconceptos";
import ModalRegistros from '../modals/registros';

class ClienteOptions extends Component {
  render() {
    const { selected } = this.props;

    return (
      <Options
        leftOps={[
          <ModalFactura isDisabled={!selected} />,
          <ModalNotaCredito isDisabled={!selected} />,
          <ModalCobro modal={false} isDisabled={!selected} />
        ]}
        rightOps={[
          <ModalPreconceptos />,
          <ModalFacturacionMasiva />,
          <ModalRegistros />
        ]}
      />
    );
  }
};


const mapStateToProps = ({ clientes }) => ({
  selected: clientes.instance
});

export default connect(mapStateToProps)(ClienteOptions);

