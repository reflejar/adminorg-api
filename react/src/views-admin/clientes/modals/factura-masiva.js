import React, { Component, Fragment } from "react";
import { Button } from "reactstrap";

import FacturacionMasiva from "../CRUDL/factura-masiva/C";
import BasicModal from '../../../components/modal/basic';

// Helpers
const initialFields = {
  desc: '',
  sellPoint: '',
  invoiceDate: '',
  transactionDate: '',
  notion: ''
};

class FacturacionMasivaModal extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      result: null,
      fields: initialFields,
      clients: [{}],
      modal: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    setTimeout(() => {
      // Emulating fetch
      this.setState(oldState => ({
        ...oldState,
        loading: false
      }));
    }, 1000);
  }

  handleChange(field) {
    return event => {
      const value = event.target.value;

      this.setState(oldState => ({
        ...oldState,
        fields: {
          ...oldState.fields,
          [field]: value
        }
      }))
    }
  }

  handleSubmit() {
    alert('See the console to se object request');
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
          header="Nueva Facturacion masiva"
          open={this.state.modal}
          onToggle={this.handleToggle}
          component={<FacturacionMasiva onClose={() => this.handleToggle(false)} />}
          button={(
            <Button
              outline
              color="primary"
              disabled={true}
              onClick={this.handleToggle}>
              Facturacion Masiva
            </Button>
          )}
        />
      </Fragment>
    );
  }
}

export default FacturacionMasivaModal;
