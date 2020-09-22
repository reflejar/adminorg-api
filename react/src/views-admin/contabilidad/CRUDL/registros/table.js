import React from 'react';
import { Table } from 'reactstrap';

class DocumentosTable extends React.Component {
    render () {
      return (
        <Table responsive borderless>
          <thead>
            <tr>
              {headers.map(h => (
                <th>{h.label}</th>
              ))}
            </tr>
          </thead>
  
          <tbody>
            {this.props.facturas.map((documento) => {
              
  
              return (
                <tr key={documento.id}>
                  <td>{documento.receipt.receipt_type}</td>
                  <td>{documento.receipt.issued_date}</td>
                  <td>{documento.receipt.point_of_sales}</td>
                  <td>{documento.receipt.receipt_number}</td>
                  <td>{documento.destinatario}</td>
                  <td>{documento.receipt.total_amount}</td>
                </tr>
              );
            })}
          </tbody>
        </Table>
      )
    }
  }

export default DocumentosTable