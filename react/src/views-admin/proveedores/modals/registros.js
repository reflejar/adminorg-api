import React, { Component } from "react";
import { Button } from "reactstrap";

import Registros from "../CRUDL/registros/index";
import BasicModal from '../../../components/modal/basic';


class ModalRegistros extends Component {
  state = {
    modal: false
  }

  handleToggle = (isOpen) => {
    this.setState({
      modal: typeof isOpen === 'boolean' ? isOpen : !this.state.modal
    });
  };

  render() {
    return (
      <BasicModal
        open={this.state.modal}
        onToggle={this.handleToggle}
        header="Registros"
        component={<Registros onClose={() => this.handleToggle(false)} />}
        button={(
          <Button
            outline
            color="purple"
            onClick={this.handleToggle}
          >
            Registros
          </Button>
        )}
      />
    );
  }
}

export default ModalRegistros;