import React from "react";

import { useIngresos } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"


const TableIngreso = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useIngresos();

  const titles = [
    {
      accessor: 'nombre',
      Header: 'Nombre'
    },
    {
      accessor: 'interes',
      Header: 'Metodo de interes'
    },
    {
      accessor: 'descuento',
      Header: 'Metodo de descuento'
    },  
  ]

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"ingreso"}
      />

  )
}


export default TableIngreso
