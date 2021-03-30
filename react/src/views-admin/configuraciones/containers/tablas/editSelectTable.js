import React, { useCallback, useState, useEffect, useMemo, useRef } from "react";

import "react-table/react-table.css";
import { Edit } from 'react-feather';
import ReactTable from 'react-table';
import ReactToPrint from 'react-to-print';
import { CSVLink } from 'react-csv';
import { Button } from 'reactstrap';
import { Printer, FileText} from "react-feather";


import Chance from "chance";

import Spinner from "../../../../components/spinner/spinner";

const chance = new Chance();

const Table = ({ titles, items, loadingItems, selectItem, toggle, causante }) => {
 

  const getColumns = useCallback(() => {
    const columns = [];
    titles.forEach(key => {
      columns.push(key);
    });
    columns.push(
      {
        Header: '',
        Cell: row => (
          
          <Edit
            size={18}
            className="mr-2"
            onClick={() => {
              selectItem({...row.original, causante});
              toggle(true)
            }}
            cursor='pointer'
          />
        )
      }
    )
    return columns;
  }, [titles, selectItem, causante, toggle])


  const [columns] = useState(getColumns())
  const [data, setData] = useState([])

  const refButton = useRef(null);

  const dataForTable = useMemo(() => {
    if (data && !data.length) {
      return [];
    }
    return data;
  }, [data]);

  useEffect(() => {

    setData(items.map(item => {
      const _id = chance.guid();
      return {
        _id,
        ...item
      };
    }))

  }, [items])

  const tableHeaders = columns.map(c => ({ label: c.Header, key: typeof c.accessor === "string" ? c.accessor : c.Header.toLowerCase() }));

  if (loadingItems) {
    return <Spinner />
  }

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
      {/* <ReactTable
        showPagination
        defaultPageSize={50}        
        data={data}
        columns={columns_final}
        sortable={false}
        className="-striped -highlight"
        {...addProps}
      /> */}
      <ReactTable
        data={data}
        columns={columns}
        defaultPageSize={50}
        className="-striped -highlight"
      />
    </React.Fragment>    
  );

}

// class Table extends Component {
//   constructor(props) {
//     super(props);
//     const columns = this.getColumns();
//     this.state = {
//       columns,
//       data: [],
//       loading: false,
//     };
//   }

  // selectEdit = async (item) => {
  //   await this.props.selectItem(item);
  //   this.props.toggle();
  // }

  // getColumns() {
  //   const columns = [];
  //   this.props.titles.forEach(key => {
  //     columns.push(key);
  //   });
  //   columns.push(
  //     {
  //       Header: '',
  //       Cell: row => (
          
  //         <Edit
  //           size={18}
  //           className="mr-2"
  //           onClick={() => this.selectEdit({...row.original, causante: this.props.causante})}
  //           cursor='pointer'
  //         />
  //       )
  //     }
  //   )
  //   return columns;
  // }



  // async componentDidMount() {
  //   const data = await this.getData();
  //   this.setState({ data })
  // }

  

  // async getData() {

  //   this.setState({ loading: true });

  //   await this.props.getItems();

  //   const data = this.props.items.map(item => {
  //     const _id = chance.guid();
  //     return {
  //       _id,
  //       ...item
  //     };
  //   });

  //   this.setState({ loading: false });

  //   return data;
  // }



//   render() {
//     const { data, columns, loading } = this.state;

//     if (loading) {
//       return <Spinner />
//     }

//     return (
//         <ReactTable
//           data={data}
//           columns={columns}
//           defaultPageSize={50}
//           className="-striped -highlight"
//         />
//     );
//   }
// }

export default Table;
