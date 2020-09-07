import React, {useMemo, useRef} from 'react';
import { connect } from 'react-redux';
import { Table, Button } from 'reactstrap';
import { CSVLink } from 'react-csv';
import ReactToPrint from 'react-to-print';
import get from 'lodash/get';

const tableHeaders = [
  { label: "Identificacion", key: "numero" },
  { label: "Propietario", key: "propietario" },
  { label: "Ocupante", key: "inquilino" },
  { label: "Domicilio", key: "domicilio" },
];
 
class DominiosTable extends React.Component {
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
          {this.props.data.map((dominio) => {

            return (
              <tr key={dominio.id}>
                <th scope="row">{dominio.numero}</th>
                <td>{dominio.propietario}</td>
                <td>{dominio.inquilino}</td>
                <td>{dominio.domicilio}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    )
  }
}


const L = ({ clientes, dominios }) => {
  const ref = useRef(null);
  
  const dataForTable = useMemo(() => {
    if (dominios && !dominios.length) {
      return [];
    }
    const data = dominios.map((dominio) => {
      const propietario = get(clientes.find((x) => x.id === dominio.propietario), 'full_name', 'Sin propietario');
      const inquilino = get(clientes.find((x) => x.id === dominio.inquilino), 'full_name', 'Sin inquilino');
      const domicilio = `${dominio.domicilio.calle} ${dominio.domicilio.numero}. ${dominio.domicilio.provincia} - ${dominio.domicilio.localidad}`
      return ({
        ...dominio,
        propietario,
        inquilino,
        domicilio
      })
    })    
    return data;
  }, [dominios, clientes]);
  
  return (
    <div className="registration__results">
      <div className="registration__actions">
        <ReactToPrint
          trigger={() => <Button outline>Imprimir</Button>}
          content={() => ref.current}
        />

        <CSVLink
          target="_blank"
          filename="dominios-clients.csv"
          headers={tableHeaders}
          data={dataForTable}>
          <Button outline>
            CSV
          </Button>
        </CSVLink>
      </div>

      <DominiosTable data={dataForTable} ref={ref} />
    </div>
  );
};

const mapStateToProps = (state) => ({
  clientes: get(state, 'clientes.list', []),
  dominios: get(state, 'dominios.list', [])
});

export default connect(mapStateToProps)(L);
