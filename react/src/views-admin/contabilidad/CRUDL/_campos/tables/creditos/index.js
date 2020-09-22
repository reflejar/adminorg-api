import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Portador', 'Ingreso', 'Periodo', 'Detalle', 'Monto'];

export const CreditosTable = ({ dataTable, errors, onlyRead }) => {
  

  return (
    <div className="CreditosTable">
      <div className="CreditosTable__header">
        {HEADERS.map((header) => (
          <span key={header} className="CreditosTable__header__item">{header}</span>
        ))}
      </div>
  
      <div className="CreditosTable__body">
        {dataTable.map((item, index) => (
          <div className="CreditosTable__body__row" key={item.vinculo}>
            <FormGroup check>
              <Label check>
                <Input
                  onChange={() => item.onRowSelect(index)}
                  name={`row_${item.vinculo}`}
                  type="checkbox"
                  disabled={onlyRead}
                  checked={onlyRead ? true : item.checked}
                />
              </Label>
            </FormGroup>
  
            <FormGroup>
              <Input
                disabled
                name="cuenta"
                value={item.cuenta}
              />
            </FormGroup>
  
            <FormGroup>
              <Input
                disabled
                name="ingreso"
                value={item.ingreso}
              />
            </FormGroup>
  
            <FormGroup>
              <Input
                disabled
                name="periodo"
                value={item.periodo}
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
                invalid={errors && errors[item.vinculo]}
                type="number"
                max={item.max}
                name="monto"
                disabled={onlyRead}
                value={item.monto}
                onChange={(event) => item.onInputChange(event, index)}
              />
  
              <FormFeedback>{errors && errors[item.vinculo]}</FormFeedback>
            </FormGroup>
          </div>
        ))}
      </div>
    </div>
  )
  
}