import React, { Component } from "react";
import { Button } from "reactstrap";

import Reportes from "../CRUDL/registros/index";
import BasicModal from '../../../components/modal/basic';


class ModalReportes extends Component {
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
        header="Reportes"
        component={<Reportes onClose={() => this.handleToggle(false)} />}
        button={(
          <Button
            outline
            color="primary"
            onClick={this.handleToggle}
          >
            Reportes
          </Button>
        )}
      />
    );
  }
}

export default ModalReportes;