import React, { Component } from "react";
import { connect } from 'react-redux';

import Options from '../../../components/board/options';
import ModalDocumento from '../modals/documento';
import ModalNotaCredito from '../modals/nota-credito';
import ModalPago from "../modals/op";
import ModalRegistros from '../modals/registros';


class ClienteOptions extends Component {
  render() {
    const { selected } = this.props;

    return (
      <Options
        leftOps={[
          <ModalDocumento isDisabled={!selected} />,
          <ModalNotaCredito isDisabled={!selected} />,
          <ModalPago isDisabled={!selected} />
        ]}
        rightOps={[
          <ModalRegistros />
        ]}
      />
    );
  }
};


const mapStateToProps = ({ proveedores }) => ({
  selected: proveedores.instance
});

export default connect(mapStateToProps)(ClienteOptions);

