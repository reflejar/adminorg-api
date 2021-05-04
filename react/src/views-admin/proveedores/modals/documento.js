import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Documento from "../CRUDL/documento/CU";
import OP from "../CRUDL/op/CU";
import BasicModal from '../../../components/modal/basic';

class ModalDocumento extends Component {
  constructor(props) {
    super(props);

    this.state = {
      modal: false,
      component: <Documento onClose={(action) => this.handleToggle(action)}/>
    };

  }

  handleToggle = (action) => {
    if (typeof action === "boolean") {
      this.setState({
        modal: !this.state.modal,
        component: <Documento onClose={(action) => this.handleToggle(action)}/>
      });
    } 
    if (action === "cobrar") {
      this.setState({
        component: <OP onClose={() => this.handleToggle(false)}/>
      });
    }
  };

  render() {
    const { isDisabled } = this.props;
    const { modal, component } = this.state;
    return (
      <Fragment>
        <BasicModal
          button={(
            <Button
              outline
              color="primary"
              disabled={isDisabled}
              onClick={() => this.handleToggle(true)}
            >
              + Comprobante
            </Button>
          )}
          open={modal}
          onToggle={() => this.handleToggle(false)}
          header="Nuevo Documento tipo factura"
          component={component}
          footer={false}
        />
      </Fragment>
    );
  }
}


export default ModalDocumento;
