import React, {useRef, useMemo} from 'react';
import ReactTable from 'react-table';
import checkboxHOC from 'react-table/lib/hoc/selectTable';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button } from 'reactstrap';
import { Printer, FileText} from "react-feather";

const CheckboxTable = checkboxHOC(ReactTable);

const TableCuenta = ({data, columns, ref, checkboxProps}) => {

  const tableHeaders = columns.map(c => ({ label: c.Header, key: c.Header.toLowerCase() }));

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
          filename="admincu-documentos.csv">
          <Button className="btn-sm" outline>
            <FileText size={18} />
          </Button>
        </CSVLink>
      </section>
      <CheckboxTable
        showPagination
        defaultPageSize={50}        
        ref={ref}
        data={data}
        columns={columns_final}
        sortable={false}
        className="-striped -highlight"
        {...checkboxProps}
      />
    </React.Fragment>
  );
};

export default TableCuenta;
