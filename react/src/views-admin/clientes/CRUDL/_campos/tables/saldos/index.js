import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Origen', 'Detalle', 'Monto'];

export const SaldosTable = ({ dataTable, errors, onlyRead }) => {
  
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
                disabled={onlyRead}
                checked={item.checked}
              />
            </Label>
          </FormGroup>

          <FormGroup>
              <Input
                disabled
                name="documento"
                value={item.documento}
              />
          </FormGroup>

          <FormGroup>
            <Input
              invalid={errors && errors[index]}
              type="text"
              placeholder="Detalle"
              name="detalle"
              disabled={onlyRead}
              value={item.detalle}
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
              disabled={onlyRead}
              value={item.monto}
              onChange={(event) => item.onInputChange(event, index)}
            />

            <FormFeedback>{errors && errors[index]}</FormFeedback>
          </FormGroup>
        </div>
      ))}
    </div>
  </div>
)}