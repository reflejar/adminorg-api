import React from "react";

import { useGastos } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"


const TableGasto = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useGastos();

  const titles = [
    {
      accessor: 'full_name',
      Header: 'Nombre'
    },
  ]  

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"gasto"}
      />

  )
}


export default TableGasto
