import React from "react";

import { useCajas } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"


const TableCaja = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useCajas();

  const titles = [
    {
      accessor: 'nombre',
      Header: 'Nombre'
    },
    {
      accessor: 'taxon',
      Header: 'Tipo'
    },
  ]

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"caja"}
      />

  )
}


export default TableCaja
