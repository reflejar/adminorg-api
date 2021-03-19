import React, {useRef, useMemo} from 'react';
import ReactTable from 'react-table';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button, ButtonGroup } from 'reactstrap';
import { Printer, FileText} from "react-feather";
import {Numero} from "../../../utility/formats";

const TableDeudas = ({data, columns, addProps}) => {

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
      <section className="bg-lighten-5 d-flex justify-content-between">
        <ButtonGroup>
          <ReactToPrint
            trigger={() => <Button className="btn-sm" outline><Printer size={18} /></Button>}
            content={() => refButton.current}
          />
          <CSVLink
            headers={tableHeaders}
            data={dataForTable}
            target="_blank"
            filename="admincu-deudas.csv">
            <Button className="btn-sm" outline>
              <FileText size={18} />
            </Button>
          </CSVLink>
        </ButtonGroup>
        <ButtonGroup>
          <div className="text-danger mr-2">
            <b>Total a pagar (+) a favor (-):</b>
          </div>
          <Button className="btn-sm btn-warning" disabled outline title="Saldo adeudado">
            {Numero(data.reduce((a,v) =>  a = a + v.saldo , 0 ))}
          </Button>            
        </ButtonGroup>
      </section>

      <ReactTable
        showPagination
        defaultPageSize={50}
        data={data}
        columns={columns_final}
        className="-striped -highlight"
        {...addProps}
      />
    </React.Fragment>
  );
};

export default TableDeudas;
