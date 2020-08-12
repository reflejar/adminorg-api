import React, { Component } from "react";

import Options from '../../../components/board/options';
import ModalTransferencia from '../modals/transferencia';
import ModalRegistros from '../modals/registros';

class CajaOptions extends Component {
  render() {

    return (
      <Options
        leftOps={[
          <ModalTransferencia />,
        ]}
        rightOps={[
          <ModalRegistros />
        ]}
      />
    );
  }
};

export default CajaOptions;

