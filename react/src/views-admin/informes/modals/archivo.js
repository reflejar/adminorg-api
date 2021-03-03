import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Archivo from "../../CRUDL/archivo/CU";
import BasicModal from '../../../components/modal/basic';

class ModalArchivo extends Component {
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
              Subir archivo
            </Button>
          )}
          header="Nuevo archivo"
          component={(<Archivo onClose={() => this.handleToggle(false)} />)}
        />
      </Fragment>
    );
  }
}

export default ModalArchivo;
