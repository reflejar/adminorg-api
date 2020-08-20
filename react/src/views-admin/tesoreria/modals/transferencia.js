import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Transferencia from "../CRUDL/transferencia/CU";
import BasicModal from '../../../components/modal/basic';

class ModalTransferencia extends Component {
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
              Transferencia entre tesoros
            </Button>
          )}
          header="Nueva Transferencia entre tesoros"
          component={(<Transferencia onClose={() => this.handleToggle(false)} />)}
        />
      </Fragment>
    );
  }
}

export default ModalTransferencia;
