import React from 'react';
import moment from 'moment';
import DeudasTable from "../../components/board/tables/deudas";

import {Numero} from "../../utility/formats";

import 'react-table/react-table.css';

const getColumns = () => [{
  Header: 'Fecha',
  id: 'Fecha',
  accessor: (d) => moment(d.fecha).format('DD/MM/YYYY')
}, {
  Header: 'Documento',
  id: 'Documento',
  accessor: 'documento.nombre',
}, {
  Header: 'Cuenta',
  accessor: "cuenta"
}, {  
  Header: 'Concepto',
  accessor: 'concepto'
}, {
  Header: 'Periodo',
  accessor: 'periodo'
}, {
  Header: 'Monto',
  accessor: 'monto',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )   
}, {
  Header: 'Pagado/Utilizado',
  accessor: 'pago_capital',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )         
}, {
  Header: 'Intereses/Descuentos',
  accessor: 'interes',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )   
}, {
  Header: 'Saldo',
  accessor: 'saldo',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )    
}];    

export default class Table extends React.Component {
  render() {
    const { data } = this.props;
    const addProps = {
      getTdProps: (state, rowInfo, column, instance) => {
        return {
          onClick: () => {
            if (rowInfo && column.id === 'Documento') {
              rowInfo.original.documento.pdf && window.open(rowInfo.original.documento.pdf, "_blank")
            }
            
          }
        }
      }
    };

    return (
      <React.Fragment>

        <DeudasTable
          data={data}
          columns={getColumns()}
          addProps={addProps}
        />     
      </React.Fragment>
    );
  }
}