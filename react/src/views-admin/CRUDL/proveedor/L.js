import React, { useMemo, useRef } from 'react';
import { CSVLink } from 'react-csv';
import { connect } from 'react-redux';
import { Table, Button } from 'reactstrap';
import get from 'lodash/get';
import ReactToPrint from 'react-to-print';

const tableHeaders = [
  'Nombre',
  'Apellido',
  'Razon social',
  'Tipo de documento',
  'Numero',
  'Mail',
  'Telefono'
];

const ProveedorStep = ({ clients }) => {
  const ref = useRef(null);

  const dataForCSV = useMemo(() => {
    if (clients && !clients.length) {
      return [];
    }

    return [
      tableHeaders,
      clients
    ];
  }, [clients]);

  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />

        <CSVLink
          target="_blank"
          filename="admincu-clients.csv"
          data={dataForCSV}>
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <ProveedoresTable data={clients} ref={ref} />
    </div>
  );
};

class ProveedoresTable extends React.Component {
  render () {
    return (
      <Table responsive borderless>
        <thead>
          <tr>
            <th>
              #
            </th>

            {tableHeaders.map(t => (
              <th key={t}>
                {t}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>

        {this.props.data.map((client) => (
          <tr key={client.id}>
            <th scope="row">{client.id}</th>
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

const mapStateToProps = (state) => ({
  clients: get(state, 'proveedores.list', [])
});

export default connect(mapStateToProps)(ProveedorStep);
