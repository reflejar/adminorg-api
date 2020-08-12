import * as React from 'react';
import { FormGroup, Input, Label, FormFeedback } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Portador', 'Ingreso', 'Periodo', 'Monto'];

export const DeudasTable = ({ dataTable, errors }) => (
  <div className="DeudasTable">
    <div className="DeudasTable__header">
      {HEADERS.map((header) => (
        <span key={header} className="DeudasTable__header__item">{header}</span>
      ))}
    </div>

    <div className="DeudasTable__body">
      {dataTable.map((item, index) => (
        <div className="DeudasTable__body__row" key={item.vinculo}>
          <FormGroup check>
            <Label check>
              <Input
                onChange={(event) => item.onRowSelect(event, item, index)}
                name={`row_${item.vinculo}`}
                type="checkbox"
                checked={item.checked}
              />
            </Label>
          </FormGroup>

          <FormGroup>
            <Input
              disabled
              name="portador"
              value={item.portador}
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
              type="number"
              name="monto"
              value={item.monto}
              onChange={(event) => item.onInputChange(event, index)}
            />

            <FormFeedback>{errors && errors[index]}</FormFeedback>
          </FormGroup>
        </div>
      ))}
    </div>
  </div>
)
