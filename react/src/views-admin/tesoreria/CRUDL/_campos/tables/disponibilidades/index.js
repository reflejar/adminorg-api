import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Origen', 'Detalle', 'Monto'];

export const DisponibilidadesTable = ({ dataTable, errors, onlyRead }) => {
  return (
  <div className="DisponibilidadesTable">
    <div className="DisponibilidadesTable__header">
      {HEADERS.map((header) => (
        <span key={header} className="DisponibilidadesTable__header__item">{header}</span>
      ))}
    </div>

    <div className="DisponibilidadesTable__body">
      {dataTable.map((item, index) => (
        <div className="DisponibilidadesTable__body__row" key={item.vinculo}>
          <FormGroup check>
            <Label check>
              <Input
                onChange={() => item.onRowSelect(index)}
                name={`row_${item.vinculo}`}
                type="checkbox"
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
                disabled
                name="detalle"
                value={item.detalle}
              />
          </FormGroup>        
          
          <FormGroup>
            <Input
              invalid={errors && errors[index]}
              type="number"
              max={item.max}
              name="monto"
              value={item.monto}
              disabled={onlyRead}
              onChange={(event) => item.onInputChange(event, index)}
            />

            <FormFeedback>{errors && errors[index]}</FormFeedback>
          </FormGroup>
        </div>
      ))}
    </div>
  </div>
)}