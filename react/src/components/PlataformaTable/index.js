import * as React from 'react';
import moment from 'moment';
import { FormGroup, Input, Label } from 'reactstrap';

import './styles.scss'

const HEADERS = ['Seleccionar', 'Plataforma', 'Fecha del pago', 'Monto'];
export const PlataformaTable = ({ dataTable, selectedItems }) => {

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
                  checked={selectedItems.some((val) => val === item.vinculo)}
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
                value={moment(item.periodo).format('YYYY-MM-DD')}
              />
            </FormGroup>

            <FormGroup>
              <Input
                disabled
                type="number"
                name="valor"
                defaultValue={item.valor}
              />
            </FormGroup>
          </div>
        ))}
      </div>
    </div>
  );
};
