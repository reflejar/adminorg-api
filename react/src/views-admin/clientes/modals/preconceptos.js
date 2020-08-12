import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import Preconceptos from "../CRUDL/preconceptos";
import BasicModal from '../../../components/modal/basic';

class ModalPreconceptos extends Component {
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
      <Fragment>
        <BasicModal
          open={this.state.modal}
          onToggle={this.handleToggle}
          button={(
            <Button
              outline
              color="primary"
              disabled={true}
              onClick={this.handleToggle}
            >
              Preconceptos
            </Button>
          )}
          // className={""}
          header="Conceptos a facturar"
          component={<Preconceptos onClose={() => this.handleToggle(false)} />}
          footer={false}
        />
      </Fragment>
    );
  }
}

export default ModalPreconceptos;
