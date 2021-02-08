import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Documento', 'Detalle', 'Monto'];

export const DebitosTable = ({ dataTable, errors, update }) => {
  

  return (
    <div className="DebitosTable">
      <div className="DebitosTable__header">
        {HEADERS.map((header) => (
          <span key={header} className="DebitosTable__header__item">{header}</span>
        ))}
      </div>
  
      <div className="DebitosTable__body">
        {dataTable.map((item, index) => (
          <div className="DebitosTable__body__row" key={item.vinculo}>
            <FormGroup check>
              <Label check>
                <Input
                  onChange={() => item.onRowSelect(index)}
                  name={`row_${item.vinculo}`}
                  type="checkbox"
                  // disabled={update}
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
                value={item.monto}
                step={0.01}
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