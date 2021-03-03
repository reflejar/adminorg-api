import React, { Component, Fragment } from "react";
import { FolderPlus } from "react-feather";

import Carpeta from "../../CRUDL/carpeta/CU";
import BasicModal from '../../../components/modal/basic';


class ModalCarpeta extends Component {
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
          button={<FolderPlus size={16} onClick={this.handleToggle} />}
          className={""}
          header={"Nueva Carpeta"}
          component={<Carpeta onClose={() => this.handleToggle(false)} />}
          footer={false}
        />
      </Fragment>
    );
  }
}

export default ModalCarpeta;