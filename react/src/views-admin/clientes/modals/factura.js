import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Factura from "../CRUDL/factura/CR";
import ReciboX from "../CRUDL/recibo-x/CR";
import BasicModal from '../../../components/modal/basic';

class ModalFactura extends Component {
  constructor(props) {
    super(props);

    this.state = {
      modal: false,
      component: <Factura onClose={(action) => this.handleToggle(action)}/>
    };

  }

  handleToggle = (action) => {
    if (typeof action === "boolean") {
      this.setState({
        modal: !this.state.modal,
        component: <Factura onClose={(action) => this.handleToggle(action)}/>
      });
    } 
    if (action === "cobrar") {
      this.setState({
        component: <ReciboX onClose={() => this.handleToggle(false)}/>
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
              + Factura
            </Button>
          )}
          open={modal}
          onToggle={() => this.handleToggle(false)}
          header="Nueva Factura"
          component={component}
          footer={false}
        />
      </Fragment>
    );
  }
}

export default ModalFactura;