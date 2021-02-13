import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Origen', 'Detalle', 'Monto'];

export const SaldosTable = ({ documento, dataTable, errors, update }) => {
  
  return (
  <div className="SaldosTable">
    <div className="SaldosTable__header">
      {HEADERS.map((header) => (
        <span key={header} className="SaldosTable__header__item">{header}</span>
      ))}
    </div>

    <div className="SaldosTable__body">
      {dataTable.map((item, index) => (
        <div className="SaldosTable__body__row" key={item.vinculo}>
          <FormGroup check>
            <Label check>
              <Input
                onChange={() => item.onRowSelect(index)}
                name={`row_${item.vinculo}`}
                type="checkbox"
                disabled={update}
                checked={item.checked}
              />
            </Label>
          </FormGroup>

          <FormGroup>
              <Input
                disabled
                name="documento"
                disabled={documento.fecha_operacion ? true: false}
                value={item.documento}
              />
          </FormGroup>

          <FormGroup>
            <Input
              invalid={errors && errors[index]}
              type="text"
              placeholder="Detalle"
              name="detalle"
              disabled={update}
              value={item.detalle}
              disabled={documento.fecha_operacion ? true: false}
              onChange={(event) => item.onInputChange(event, index)}
            />

            <FormFeedback>{errors && errors[index]}</FormFeedback>
          </FormGroup>          

          <FormGroup>
            <Input
              invalid={errors && errors[index]}
              type="number"
              max={item.max}
              name="monto"
              disabled={update}
              value={item.monto}
              disabled={documento.fecha_operacion ? true: false}
              onChange={(event) => item.onInputChange(event, index)}
            />

            <FormFeedback>{errors && errors[index]}</FormFeedback>
          </FormGroup>
        </div>
      ))}
    </div>
  </div>
)}