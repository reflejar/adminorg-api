import * as React from 'react';
import { FormGroup, Input, Label, Table } from 'reactstrap';

import './styles.scss'

const preconceptosHeaders = ['Destinatario', 'Ingreso', 'Periodo', 'Detalle', 'Fecha V', 'Fecha G', 'Monto'];


export const PreconceptosTable = ({ dataTable, all, onAllSelect }) => {
  

  return (
    <div className="PreconceptosTable">
      <Table>
        <thead>
          <tr>
            <th>
              <FormGroup check>
                <Label check>
                  <Input
                    type="checkbox"
                    onChange={() => onAllSelect()}
                    checked={all}
                  />
                </Label>
              </FormGroup>
            </th>            
            {preconceptosHeaders.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {dataTable.map((row, index) => {

            return (
              <tr key={index}>
                <td>
                  <FormGroup check style={{ display: 'flex' }}>
                    <Label check>
                      <Input
                        type="checkbox"
                        onChange={() => row.onRowSelect(index)}
                        checked={row.checked}
                      />
                    </Label>
                  </FormGroup>
                </td>
                <td>{row.destinatario}</td>
                <td>{row.concepto}</td>
                <td>{row.periodo}</td>
                <td>{row.detalle}</td>
                <td>{row.fecha_vencimiento}</td>
                <td>{row.fecha_gracia}</td>
                <td>{row.monto}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </div>
  )
  
}