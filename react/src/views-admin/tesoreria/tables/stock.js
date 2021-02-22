import React from 'react';
import ReactTable from 'react-table';
import DeudasTable from "../../../components/board/tables/deudas";
import {Numero} from "../../../utility/formats";

import BasicModal from '../../../components/modal/basic';
import Comprobante from '../CRUDL/transferencia/CU';

import 'react-table/react-table.css';

export default class Table extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selection: [],
            selectAll: false,
            modal: {
                open: false,
                item: null
            }
          };

    }

    getColumns = (selected) => [{
      id: 'Portador',
      Header: 'Portador',
      accessor: () => `${selected.full_name}`
    }, {
      id: 'Documento',
      Header: 'Documento',
      accessor: (d) => `${d.documento.receipt.receipt_type} ${d.documento.receipt.formatted_number}`
    }, {
      Header: 'Monto',
      accessor: 'monto',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )         
    }, {
      Header: 'Utilizado',
      accessor: 'pago_total',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )         
    }, {
      Header: 'Saldo',
      accessor: 'saldo',
  Cell: row => (
    <div
      style={{
        width: '100%',
        textAlign: "right"
      }}
    >
      {Numero(row.value)}
    </div>
  )         
    }];    

  toggleAll = () => {
    /*
      'toggleAll' is a tricky concept with any filterable table
      do you just select ALL the records that are in your data?
      OR
      do you only select ALL the records that are in the current filtered data?

      The latter makes more sense because 'selection' is a visual thing for the user.
      This is especially true if you are going to implement a set of external functions
      that act on the selected information (you would not want to DELETE the wrong thing!).

      So, to that end, access to the internals of ReactTable are required to get what is
      currently visible in the table (either on the current page or any other page).

      The HOC provides a method call 'getWrappedInstance' to get a ref to the wrapped
      ReactTable and then get the internal state and the 'sortedData'.
      That can then be iterrated to get all the currently visible records and set
      the selection state.
    */
    const selectAll = this.state.selectAll ? false : true;
    const selection = [];
    if (selectAll) {
      // we need to get at the internals of ReactTable
      const wrappedInstance = this.checkboxTable.getWrappedInstance();
      // the 'sortedData' property contains the currently accessible records based on the filter and sort
      const currentRecords = wrappedInstance.getResolvedState().sortedData;
      // we just push all the IDs onto the selection array
      currentRecords.forEach(item => {
        selection.push(item._original._id);
      });
    }
    this.setState({ selectAll, selection });
  };

  isSelected = key => {
    /*
      Instead of passing our external selection state we provide an 'isSelected'
      callback and detect the selection state ourselves. This allows any implementation
      for selection (either an array, object keys, or even a Javascript Set object).
    */
    return this.state.selection.includes(key);
  };

  handleToggle = (rowInfo) => {
    this.setState({
      ...this.state,
      modal: {
        open: !this.state.modal.open,
        item: rowInfo.original
      }
    });
  };

  selectDocument = (type) => {
    const { documento } = this.state.modal.item;
    const documentos = {
      "Comprobante C": <Comprobante
        onlyRead={true}
        onClose={this.handleToggle}
        selected={documento}
      />

    }
    return documentos[type]
  }

  renderModal = () => {
    const { item } = this.state.modal;
    if (item && item.documento) {
      const { receipt } = item.documento
      return (
          <BasicModal
            open={this.state.modal.open}
            onToggle={this.handleToggle}
            header={`${receipt.receipt_type} - ${receipt.formatted_number}`}
            footer={false}
            component={this.selectDocument(item.documento.receipt.receipt_type)}
          />          
        )
    } 
  }

  render() {
    const { toggleSelection, toggleAll, isSelected } = this;
    const { selectAll } = this.state;
    const { data, selected } = this.props;

    const checkboxProps = {
      selectAll,
      isSelected,
      toggleSelection,
      toggleAll,
      selectType: "checkbox",
      getTdProps: (state, rowInfo, column, instance) => {
        return {
          onClick: () => {
            if (rowInfo && column.id === 'Documento') {
              this.handleToggle(rowInfo);
            }
          }
        }
      },
      getTrProps: (s, r) => {
        // someone asked for an example of a background color change
        // here it is...
        let selected;
        if (r) {
          selected = this.isSelected(r.original._id);
        }
        return {
          style: {
            backgroundColor: selected ? "lightgreen" : "inherit",
          }
        };
      }
    };

    return (
      <React.Fragment>
        {this.state.modal && this.state.modal.item && this.renderModal()}

        <DeudasTable
          data={data}
          columns={this.getColumns(selected)}
          ref={r => (this.checkboxTable = r)}
          checkboxProps={checkboxProps}
        /> 
      </React.Fragment>
    );
  }
}