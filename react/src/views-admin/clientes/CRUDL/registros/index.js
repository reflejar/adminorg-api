import React, { Component } from 'react';

import {User, Home, FileText} from "react-feather";
// Components
import { Row, Col, Button } from 'reactstrap';
import MinimalStatistics from "../../../../components/cards/minimalStatisticsCard2";

import Clientes from '../../../CRUDL/cliente/L';
import Dominios from '../../../CRUDL/dominio/L';
import Documentos from "../../../CRUDL/documento/L";
import { facturasTypes, notasCreditoTypes, notasDebitoTypes, recibosTypes } from '../_options/receipt_types';

// SCSS
import './index.scss';

const options = [
    {
      nombre: "Clientes",
      icono: <User size={56} strokeWidth="1.3" className="primary" />
    },
    {
      nombre: "Dominios",
      icono: <Home size={56} strokeWidth="1.3" className="primary" />
    },
    {
      nombre: "Documentos",
      icono: <FileText size={56} strokeWidth="1.3" className="primary" />
    },        
];
// [
//   'Clientes',
//   'Dominios',
//   'Documentos',
// ];

class Registros extends Component {
  constructor(props) {
    super(props);

    this.state = {
      previousStep: 0,
      step: 0,
      type: null,
      documentosTypes: [...facturasTypes, ...notasCreditoTypes, ...notasDebitoTypes, ...recibosTypes]
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
    const { step, type, documentosTypes } = this.state;

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

        {step === 2 && type === 0 && <Clientes />}
        {step === 2 && type === 1 && <Dominios />}
        {step === 1 && type === 2 && <Documentos causante={"cliente"} documentosTypes={documentosTypes} />}
        
        <Button onClick={this.handlePreviousStep} disabled={!step} color="warning">
          Volver
        </Button>
      </div>
    );
  }
}

export default Registros;