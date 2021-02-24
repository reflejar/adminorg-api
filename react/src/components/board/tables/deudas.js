import React, {useRef, useMemo} from 'react';
import ReactTable from 'react-table';
import checkboxHOC from 'react-table/lib/hoc/selectTable';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button } from 'reactstrap';
import { Printer, FileText} from "react-feather";
import {Numero} from "../../../utility/formats";

const CheckboxTable = checkboxHOC(ReactTable);

const TableDeudas = ({data, columns, ref, checkboxProps}) => {

  const tableHeaders = columns.map(c => ({ label: c.Header, key: typeof c.accessor === "string" ? c.accessor : c.Header.toLowerCase() }));

  const dataForTable = useMemo(() => {
    if (data && !data.length) {
      return [];
    }
    return data;
  }, [data]);

  const refButton = useRef(null);
  return (
    <React.Fragment>
      <div className="row">
        <div className="col-sm-6">
          <div className="bg-lighten-5 text-left">
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

          </div>
        </div>
        <div className="col-sm-6">
          <div className="row">
            <div className="col-sm-9 text-right">
              Saldo total:
            </div>
            <div className='form-group col-md-3'>
              <Button className="btn-sm" disabled outline>
                {Numero(data.reduce((a,v) =>  a = a + v.saldo , 0 ))}
              </Button>            
            </div>
          </div>
        </div>
      </div>
      <CheckboxTable
        showPagination
        defaultPageSize={50}
        ref={ref}
        data={data}
        defaultSorted={[
          {
            id: "Fecha",
            desc: true
          }
        ]}
        columns={columns}
        className="-striped -highlight"
        {...checkboxProps}
      />
    </React.Fragment>
  );
};

export default TableDeudas;
