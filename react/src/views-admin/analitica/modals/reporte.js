import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Reporte from "../CRUDL/reporte/C";
import BasicModal from '../../../components/modal/basic';

class ModalReporte extends Component {
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
              Crear reporte
            </Button>
          )}
          header="Nuevo reporte"
          component={(<Reporte onClose={() => this.handleToggle(false)} />)}
        />
      </Fragment>
    );
  }
}

export default ModalReporte;
