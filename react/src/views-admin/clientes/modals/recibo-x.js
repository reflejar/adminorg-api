import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import ReciboX from "../CRUDL/recibo-x/CR";
import BasicModal from '../../../components/modal/basic';


class ModalReciboX extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      modal: false
    };
    
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
              + Cobro
            </Button>
          )}
          header="Nuevo cobro"
          component={(<ReciboX onClose={() => this.handleToggle(false)} />)}
        />
      </Fragment>
    );
  }
}

export default ModalReciboX;
