import React from 'react';
import moment from "moment";
import DeudasTable from "../../../components/board/tables/deudas";
import {Numero} from "../../../utility/formats";

import BasicModal from '../../../components/modal/basic';

// Cosas de Clientes
import ClienteComprobante from '../../clientes/CRUDL/factura/CR';
import ClienteNotaCredito from '../../clientes/CRUDL/nota-credito/CR';
import ClienteReciboX from '../../clientes/CRUDL/recibo-x/CR';
import { 
  facturasTypes as clientesComprobantesTypes, 
  notasCreditoTypes as clientesNotasCreditoTypes, 
  notasDebitoTypes as clientesNotasDebitoTypes, 
  recibosTypes as clientesRecibosTypes 
} from '../../clientes/CRUDL/_options/receipt_types';

// Cosas de Proveedores
import ProveedorDocumento from '../../proveedores/CRUDL/documento/CU';
import ProveedorNotaCredito from '../../proveedores/CRUDL/nota-credito/CU';
import ProveedorOP from '../../proveedores/CRUDL/op/CU';
import { 
  documentosTypes as proveedoresDocumentosTypes, 
  notasCreditoTypes as proveedoresNotasCreditoTypes, 
  opTypes as proveedoresOpTypes
 } from '../../proveedores/CRUDL/_options/receipt_types';

// Cosas de Tesoreria
import TesoreriaTransferencia from '../CRUDL/transferencia/CU';
import { 
  transferenciasTypes as tesoreriaTransferenciasTypes, 
 } from '../CRUDL/_options/receipt_types';


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

  selectDocument = (causante, type) => {
    const { documento } = this.state.modal.item;
    let documentos = {};
    if (causante === "cliente") {
      clientesComprobantesTypes.forEach((type) => {
        documentos[type.nombre] = <ClienteComprobante
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      clientesNotasDebitoTypes.forEach((type) => {
        documentos[type.nombre] = <ClienteComprobante
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      clientesNotasCreditoTypes.forEach((type) => {
        documentos[type.nombre] = <ClienteNotaCredito
        destinatario={documento.destinatario}
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      clientesRecibosTypes.forEach((type) => {
        documentos[type.nombre] = <ClienteReciboX
        destinatario={documento.destinatario}
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      return documentos[type]
    }
    if (causante === "proveedor") {
      proveedoresDocumentosTypes.forEach((type) => {
        documentos[type.nombre] = <ProveedorDocumento
        destinatario={documento.destinatario}
        update={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      proveedoresNotasCreditoTypes.forEach((type) => {
        documentos[type.nombre] = <ProveedorNotaCredito
        destinatario={documento.destinatario}
        update={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      proveedoresOpTypes.forEach((type) => {
        documentos[type.nombre] = <ProveedorOP
        destinatario={documento.destinatario}
        update={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      return documentos[type]
    }
    if (causante === "caja") {
      tesoreriaTransferenciasTypes.forEach((type) => {
        documentos[type.nombre] = <TesoreriaTransferencia
        update={true}
        onClose={this.handleToggle}
        selected={documento}
      />
      })
      return documentos[type]
    }    
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
            component={this.selectDocument(item.causante, item.documento.receipt.receipt_type)}
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