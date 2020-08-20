import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import OP from "../CRUDL/op/CU";
import BasicModal from '../../../components/modal/basic';

class ModalPago extends Component {
  state = {
    modal: false
  }

  handleToggle = (isOpen) => {
    this.setState({
      modal: typeof isOpen === 'boolean' ? isOpen : !this.state.modal
    });
  };

  render() {
    const { isDisabled } = this.props;

    return (
      <Fragment>
        <BasicModal
          open={this.state.modal}
          onToggle={this.handleToggle}
          button={(
            <Button
              outline
              color="primary"
              disabled={isDisabled}
              onClose={() => this.handleToggle(false)}
            >
              Agregar Pago
            </Button>
          )}
          header="Nuevo Pago"
          component={(<OP onClose={() => this.handleToggle(false)} />)}
        />
      </Fragment>
    );
  }
}

export default ModalPago;
