import React, { Component, Fragment } from "react";
import { UserPlus } from "react-feather";

import Cliente from "../../CRUDL/cliente/CU";
import BasicModal from '../../../components/modal/basic';


class ModalCliente extends Component {
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
          button={<UserPlus size={16} onClick={this.handleToggle} />}
          className={""}
          header={"Nuevo Cliente"}
          component={<Cliente onClose={() => this.handleToggle(false)} />}
          footer={false}
        />
      </Fragment>
    );
  }
}

export default ModalCliente;