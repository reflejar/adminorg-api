import React, { useCallback, useState, useEffect } from "react";

import ReactTable from "react-table";
import "react-table/react-table.css";
import { Edit } from 'react-feather';



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
              toggle()
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


  useEffect(() => {

    setData(items.map(item => {
      const _id = chance.guid();
      return {
        _id,
        ...item
      };
    }))

  }, [items])



  if (loadingItems) {
    return <Spinner />
  }

  return (
      <ReactTable
        data={data}
        columns={columns}
        defaultPageSize={50}
        className="-striped -highlight"
      />
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
