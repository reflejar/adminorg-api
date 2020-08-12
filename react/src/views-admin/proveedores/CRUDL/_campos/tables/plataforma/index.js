import * as React from 'react';
import { FormGroup, Input, Label } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Plataforma', 'Fecha del pago', 'Monto'];
export const PlataformaTable = ({ dataTable, errors, onlyRead }) => {

  return (
    <div className="PlataformaTable">
      <div className="PlataformaTable__header">
        {HEADERS.map((header) => (
          <span key={header} className="PlataformaTable__header__item">{header}</span>
        ))}
      </div>

      <div className="PlataformaTable__body">
        {dataTable.map((item) => (
          <div className="PlataformaTable__body__row" key={item.vinculo}>
            <FormGroup check>
              <Label check>
                <Input
                  onChange={item.onRowSelect(item)}
                  name={`row_${item.vinculo}`}
                  type="checkbox"
                  checked={item.checked}
                />
              </Label>
            </FormGroup>

            <FormGroup>
              <Input
                disabled
                name="name"
                value={item.name}
              />
            </FormGroup>

            <FormGroup>
              <Input
                disabled
                name="periodo"
                value={item.fecha}
              />
            </FormGroup>

            <FormGroup>
              <Input
                disabled
                type="number"
                name="monto"
                defaultValue={item.monto}
              />
            </FormGroup>
          </div>
        ))}
      </div>
    </div>
  );
};
