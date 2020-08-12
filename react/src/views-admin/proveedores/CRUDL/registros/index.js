import React, { Component } from 'react';

// Components
import { Button } from 'reactstrap';
import Proveedores from '../../../CRUDL/proveedor/L';
import Documentos from "../../../CRUDL/documento/L";
import { documentosTypes, notasCreditoTypes, opTypes } from '../_options/receipt_types';

// SCSS
import './index.scss';

const options = [
  'Proveedores',
  'Documentos',
];

class Registros extends Component {
  constructor(props) {
    super(props);

    this.state = {
      previousStep: 0,
      step: 0,
      type: null,
      allDocumentosTypes: [...documentosTypes, ...notasCreditoTypes, ...opTypes]
    };

    this.handlePreviousStep = this.handlePreviousStep.bind(this);
    this.handleSelectType = this.handleSelectType.bind(this);
    this.handleFinish = this.handleFinish.bind(this);
  }

  handlePreviousStep () {
    this.setState(oldState => ({
      ...oldState,
      step: oldState.previousStep
    }));
  };

  handleSelectType (idx) {
    return () => {
      if (idx !== 0 && idx !== 1) {
        return this.setState(oldState => ({
          ...oldState,
          step: oldState.step + 1,
          previousStep: oldState.step,
          type: idx
        }))
      }

      this.setState(oldState => ({
        ...oldState,
        step: 2,
        previousStep: oldState.step,
        type: idx
      }));
    }
  };

  handleFinish () {
    alert('You just finish the process!');
  }


  render () {
    const { step, type, allDocumentosTypes } = this.state;

    return (
      <div className="registration">
        {step === 0 && (
          <div className="registration__type">
            {options.map((option , idx) => (
              <Button color="primary" key={idx} onClick={this.handleSelectType(idx)}>
                {option}
              </Button>
            ))}
          </div>
        )}
        {step === 2 && type === 0 && <Proveedores />}
        {step === 2 && type === 1 && <Documentos causante={"proveedor"} documentosTypes={allDocumentosTypes} />}
        
        <Button onClick={this.handlePreviousStep} disabled={!step} color="warning">
          Volver
        </Button>
      </div>
    );
  }
}

export default Registros;