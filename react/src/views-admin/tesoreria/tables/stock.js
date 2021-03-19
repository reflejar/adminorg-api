import React from 'react';
import moment from "moment";
import DeudasTable from "../../../components/board/tables/deudas";
import {Numero} from "../../../utility/formats";

import BasicModal from '../../../components/modal/basic';
import Comprobante from '../CRUDL/transferencia/CU';

import 'react-table/react-table.css';

const getColumns = () => [{
  Header: 'Fecha',
  id: 'Fecha',
  accessor: (d) => moment(d.fecha).format('DD/MM/YYYY')
}, {
  id: 'Documento',
  Header: 'Documento',
  accessor: 'documento.nombre'
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
  Header: 'Utilizado',
  accessor: 'pago_total',
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
    constructor(props) {
        super(props);

        this.state = {
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

  selectDocument = (type) => {
    const { documento } = this.state.modal.item;
    const documentos = {
      "Comprobante C": <Comprobante
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />

    }
    return documentos[type]
  }

  renderModal = () => {
    const { item } = this.state.modal;
    if (item && item.documento) {
      const { receipt } = item.documento
      return (
          <BasicModal
            open={this.state.modal.open}
            onToggle={this.handleToggle}
            header={`${receipt.receipt_type} - ${receipt.formatted_number}`}
            footer={false}
            component={this.selectDocument(item.documento.receipt.receipt_type)}
          />          
        )
    } 
  }

  render() {
    const { data } = this.props;

    const addProps = {
      getTdProps: (state, rowInfo, column, instance) => {
        return {
          onClick: () => {
            if (rowInfo && column.id === 'Documento') {
              this.handleToggle(rowInfo);
            }
            
          }
        }
      }
    };
        
    return (
      <React.Fragment>
        {this.state.modal && this.state.modal.item && this.renderModal()}

        <DeudasTable
          data={data}
          columns={getColumns()}
          addProps={addProps}
        /> 
      </React.Fragment>
    );
  }
}