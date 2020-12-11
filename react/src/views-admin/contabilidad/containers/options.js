import React from "react";

import ModalAsiento from '../modals/asiento';
import ModalRegistros from '../modals/reportes';

import { ButtonGroup } from "reactstrap";

const Options = () => {

    return (
        <section className="chat2-app-form bg-blue-grey bg-lighten-5 d-flex justify-content-between">
          <ButtonGroup>
            <ModalAsiento />
          </ButtonGroup>

          <ButtonGroup>
            <ModalRegistros />
          </ButtonGroup>
        </section>
    );
  }

export default Options;

