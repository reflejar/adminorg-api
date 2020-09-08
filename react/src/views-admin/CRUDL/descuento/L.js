import React, { useMemo, useRef } from 'react';
import { CSVLink } from 'react-csv';
import { connect } from 'react-redux';
import { Table, Button } from 'reactstrap';
import get from 'lodash/get';
import ReactToPrint from 'react-to-print';

const tableHeaders = [
  'Nombre',
  'Tipo'
];

const CajaStep = ({ cajas }) => {
  const ref = useRef(null);

  const dataForCSV = useMemo(() => {
    if (cajas && !cajas.length) {
      return [];
    }

    return [
      tableHeaders,
      cajas
    ];
  }, [cajas]);

  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />

        <CSVLink
          target="_blank"
          filename="admincu-cajas.csv"
          data={dataForCSV}>
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <CajasTable data={cajas} ref={ref} />
    </div>
  );
};

class CajasTable extends React.Component {
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

        {this.props.data.map((caja) => (
          <tr key={caja.id}>
            <th scope="row">{caja.id}</th>
            <td>{caja.nombre}</td>
            <td>{caja.taxon}</td>
          </tr>
        ))}
        </tbody>
      </Table>
    )
  }
}

const mapStateToProps = (state) => ({
  cajas: get(state, 'cajas.list', [])
});

export default connect(mapStateToProps)(CajaStep);
