import React, { Component, Fragment } from "react";
import { UserPlus } from "react-feather";

import Caja from "../../CRUDL/caja/CU";
import BasicModal from '../../../components/modal/basic';


class ModalCaja extends Component {
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
          header={"Nueva Caja"}
          component={<Caja onClose={() => this.handleToggle(false)} />}
          footer={false}
        />
      </Fragment>
    );
  }
}

export default ModalCaja;