import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Retencion', 'Detalle', 'Monto'];

export const RetencionesTable = ({ dataTable, errors, onlyRead }) => {
  return (
  <div className="RetencionesTable">
    <div className="RetencionesTable__header">
      {HEADERS.map((header) => (
        <span key={header} className="RetencionesTable__header__item">{header}</span>
      ))}
    </div>

    <div className="RetencionesTable__body">
      {dataTable.map((item, index) => (
        <div className="RetencionesTable__body__row" key={item.retencion}>
          <FormGroup check>
            <Label check>
              <Input
                onChange={() => item.onRowSelect(index)}
                name={`row_${item.retencion}`}
                type="checkbox"
                checked={item.checked}
              />
            </Label>
          </FormGroup>

          <FormGroup>
              <Input
                disabled
                name="tipo"
                value={item.tipo}
              />
          </FormGroup>

          <FormGroup>
            <Input
              invalid={errors && errors[index]}
              type="text"
              placeholder="Detalle"
              name="detalle"
              value={item.detalle}
              disabled={onlyRead}
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