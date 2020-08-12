import React, { useMemo, useRef } from 'react';
import { CSVLink } from 'react-csv';
import { connect } from 'react-redux';
import { Table, Button } from 'reactstrap';
import get from 'lodash/get';
import ReactToPrint from 'react-to-print';

const tableHeaders = [
  { label: "Nombre", key: "perfil.nombre" },
  { label: "Apellido", key: "perfil.apellido" },
  { label: "Razon social", key: "perfil.razon_social" },
  { label: "Tipo de documento", key: "perfil.tipo_documento" },
  { label: "Numero", key: "perfil.numero_documento" },
  { label: "Mail", key: "perfil.mail" },
  { label: "Telefono", key: "perfil.telefono" },
];
 

class ClientesTable extends React.Component {
  render () {
    return (
      <Table responsive borderless>
        <thead>
          <tr>

            {tableHeaders.map(t => (
              <th key={t.key}>
                {t.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>

        {this.props.data.map((client) => (
          <tr key={client.id}>
            <td>{client.perfil.nombre}</td>
            <td>{client.perfil.apellido}</td>
            <td>{client.perfil.razon_social}</td>
            <td>{client.perfil.tipo_documento}</td>
            <td>{client.perfil.numero_documento}</td>
            <td>{client.perfil.mail}</td>
            <td>{client.perfil.telefono}</td>
          </tr>
        ))}
        </tbody>
      </Table>
    )
  }
}


const L = ({ clientes }) => {
  const ref = useRef(null);

  const dataForTable = useMemo(() => {
    if (clientes && !clientes.length) {
      return [];
    }
    return clientes;
  }, [clientes]);

  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />

        <CSVLink
          target="_blank"
          filename="admincu-clientes.csv"
          headers={tableHeaders}          
          data={dataForTable}>
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <ClientesTable data={dataForTable} ref={ref} />
    </div>
  );
};

const mapStateToProps = (state) => ({
  clientes: get(state, 'clientes.list', [])
});

export default connect(mapStateToProps)(L);
