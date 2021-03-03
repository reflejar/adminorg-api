import React, { Component } from "react";

import Options from '../../../components/board/options';
import ModalReporte from '../modals/reporte';
import ModalArchivo from '../modals/archivo';


class ClienteOptions extends Component {
  render() {

    return (
      <Options
        leftOps={[
          <ModalReporte isDisabled={false} />,
          <ModalArchivo isDisabled={false} />,
        ]}
        rightOps={[
          // <ModalRegistros />
        ]}
      />
    );
  }
};



export default ClienteOptions;

