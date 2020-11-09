import React, { Component } from 'react';

// Components
import { Row, Col, Button } from 'reactstrap';
import {Briefcase, FileText} from "react-feather";
import MinimalStatistics from "../../../../components/cards/minimalStatisticsCard2";

import Cajas from '../../../CRUDL/caja/L';
import Documentos from "../../../CRUDL/documento/L";
import { transferenciasTypes } from '../_options/receipt_types';

// SCSS
import './index.scss';

const options = [
  {
    nombre: "Cajas",
    icono: <Briefcase size={56} strokeWidth="1.3" className="primary" />
  },
  {
    nombre: "Documentos",
    icono: <FileText size={56} strokeWidth="1.3" className="primary" />
  },        
];

class Registros extends Component {
  constructor(props) {
    super(props);

    this.state = {
      previousStep: 0,
      step: 0,
      type: null,
      allDocumentosTypes: [...transferenciasTypes]
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
          <Row>
            {options.map((option , idx) => (
              <Col sm="12" md="4" key={idx} >
                <MinimalStatistics onClick={this.handleSelectType(idx)} statistics={option.nombre} statisticsColor="primary" iconSide="right">
                  {option.icono}
                </MinimalStatistics>
              </Col>

            ))}
          </Row>
        </div>
        )}
        {step === 2 && type === 0 && <Cajas />}
        {step === 2 && type === 1 && <Documentos causante={"tesoreria"} documentosTypes={allDocumentosTypes} />}
        
        <Button onClick={this.handlePreviousStep} disabled={!step} color="warning">
          Volver
        </Button>
      </div>
    );
  }
}

export default Registros;