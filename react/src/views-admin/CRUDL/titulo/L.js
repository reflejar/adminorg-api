import React, {useMemo, useRef} from 'react';
import { connect } from 'react-redux';
import { Table, Button } from 'reactstrap';
import { CSVLink } from 'react-csv';
import ReactToPrint from 'react-to-print';
import get from 'lodash/get';

const tableHeaders = [
  { label: "Nombre", key: "nombre" },
];
 
class GastosTable extends React.Component {
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
          {this.props.data.map((gasto) => {

            return (
              <tr key={gasto.id}>
                <th scope="row">{gasto.nombre}</th>
              </tr>
            );
          })}
        </tbody>
      </Table>
    )
  }
}


const L = ({ gastos }) => {
  const ref = useRef(null);
  
  const dataForTable = useMemo(() => {
    if (gastos && !gastos.length) {
      return [];
    }
    const data = gastos;
    return data;
  }, [gastos]);
  
  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />

        <CSVLink
          target="_blank"
          filename="gastos.csv"
          headers={tableHeaders}
          data={dataForTable}>
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <GastosTable data={dataForTable} ref={ref} />
    </div>
  );
};

const mapStateToProps = (state) => ({
  gastos: get(state, 'gastos.list', [])
});

export default connect(mapStateToProps)(L);
