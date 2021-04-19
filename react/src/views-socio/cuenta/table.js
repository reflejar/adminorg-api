import React from 'react';
import moment from 'moment';
import CuentaTable from "../../components/board/tables/cuenta";

import config from "../../redux/config/config";

import {Numero} from "../../utility/formats";

import 'react-table/react-table.css';

const getColumns = () => [{
  Header: 'Fecha',
  id: 'Fecha',
  accessor: (d) => moment(d.fecha).format('DD/MM/YYYY')
}, {
  Header: 'Documento',
  id: 'Documento',
  accessor: 'documento.nombre'
}, {
  Header: 'Cuenta',
  accessor: 'cuenta'  
}, {
  Header: 'Concepto',
  accessor: 'concepto'
}, {
  Header: 'Periodo',
  id: 'Periodo',
  accessor: 'periodo'
}, {
  Header: 'Valor',
  accessor: 'valor',
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
              rowInfo.original.documento.pdf && window.open(config.baseUrl.slice(0,-1) + rowInfo.original.documento.pdf, "_blank")
            }
            
          }
        }
      }
    };

    return (
      <React.Fragment>

        <CuentaTable
          data={data}
          columns={getColumns()}
          addProps={addProps}
        />     
      </React.Fragment>
    );
  }
}