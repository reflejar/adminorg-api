import React, {useRef, useMemo} from 'react';
import ReactTable from 'react-table';
import checkboxHOC from 'react-table/lib/hoc/selectTable';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button } from 'reactstrap';
import { Printer, FileText} from "react-feather";

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
