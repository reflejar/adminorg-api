import React from 'react';
import moment from 'moment';
import OperacionTable from "../../../components/board/tables/operacion";
import {Numero} from "../../../utility/formats";

import 'react-table/react-table.css';


const getColumns = () => [{
  Header: 'Fecha',
  id: 'Fecha',
  accessor: (d) => moment(d.fecha).format('DD/MM/YYYY')
}, {
  Header: 'N° Titulo',
  accessor: 'titulo_numero'
}, {        
  Header: 'Titulo',
  accessor: 'titulo_nombre'
}, {          
  Header: 'Cuenta',
  accessor: 'cuenta'
}, {
  Header: 'Concepto',
  accessor: 'concepto'
}, {      
  Header: 'Periodo',
  accessor: 'periodo'
}, {    
  Header: 'Tipo Doc',
  accessor: 'documento_tipo'
}, {            
  Header: 'Doc N°',
  accessor: 'documento_numero'
}, {   
  Header: 'Cantidad',
  accessor: 'cantidad'
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
  Header: 'Debe',
  accessor: 'debe',
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
  Header: 'Haber',
  accessor: 'haber',
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
  Header: 'S. Capital',
  accessor: 'capital',
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
  Header: 'S. Interes',
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
  Header: 'S. Total',
  accessor: 'total',
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
  constructor(props) {
    super(props);

    this.state = {
      columns: getColumns(),
      selection: [],
      selectAll: false,
      modal: {
        open: false,
        item: null
      }
    };
  }

  handleToggle = (rowInfo) => {
    this.setState({
      ...this.state,
      modal: {
        open: !this.state.modal.open,
        item: rowInfo.original
      }
    });
  };


  render() {
    const { data } = this.props;
    return (
      <React.Fragment>
        {this.state.modal && this.state.modal.item && this.renderModal()}
        <OperacionTable
          data={data}
          columns={getColumns()}
        />   
      </React.Fragment>
    );
  }
}