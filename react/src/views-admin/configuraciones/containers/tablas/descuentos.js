import React from "react";
import get from 'lodash/get';

import { useDescuentos } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"
import { tipos } from '../../../../utility/options/metodos';


const TableDescuentos = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useDescuentos();

  const titles = [
    {
      accessor: 'nombre',
      Header: 'Nombre'
    },
    {
      id: 'Tipo',
      accessor: (d) => get(tipos.find((x) => d.tipo === x.id), 'nombre'),
      Header: 'Tipo'
    },
    {
      accessor: 'plazo',
      Header: 'Plazo estipulado'
    },  
    {
      accessor: 'monto',
      Header: 'Monto'
    },    
  ]

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"descuento"}
      />

  )
}


export default TableDescuentos