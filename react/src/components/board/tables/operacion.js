import React, {useRef, useMemo} from 'react';
import ReactTable from 'react-table';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button } from 'reactstrap';
import { Printer, FileText} from "react-feather";

const TableOperacion = ({data, columns}) => {

  const tableHeaders = columns.map(c => ({ label: c.Header, key: typeof c.accessor === "string" ? c.accessor : c.Header.toLowerCase() }));

  const dataForTable = useMemo(() => {
    if (data && !data.length) {
      return [];
    }
    return data;
  }, [data]);

  const refButton = useRef(null);
  const columns_final = columns.map(c => {
    if (c.Header === "Documento") {
      return ({...c, Cell: rowData => (
        <div
          className={rowData.row._original.documento.fecha_anulacion && "text-danger" }
          style={{
            cursor:"pointer"
          }}
        >
          {rowData.value}
        </div>
      )   })
    }
    return ({...c})
  })
  return (
    <React.Fragment>
      <section className="bg-lighten-5 text-left">
        <ReactToPrint
          trigger={() => <Button className="btn-sm" outline><Printer size={18} /></Button>}
          content={() => refButton.current}
        />
        <CSVLink
          headers={tableHeaders}
          data={dataForTable}
          target="_blank"
          filename="admincu-cuenta.csv">
          <Button className="btn-sm" outline>
            <FileText size={18} />
          </Button>
        </CSVLink>
      </section>
      <ReactTable
        showPagination
        defaultPageSize={100}        
        data={data}
        columns={columns_final}
        className="-striped -highlight"
      />
    </React.Fragment>
  );
};

export default TableOperacion;
