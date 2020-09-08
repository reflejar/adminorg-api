import React from "react";
import get from 'lodash/get';

import { useIntereses } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"
import { tipos, periodizaciones } from '../../../../utility/options/metodos';


const TableIntereses = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useIntereses();

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
    {
      id: 'Base de calculo',
      accessor: (d) => get(periodizaciones.find((x) => d.base_calculo === x.id), 'nombre'),
      Header: 'Base de calculo'
    },      
    {
      id: 'Tipo de reconocimiento',
      accessor: (d) => get(periodizaciones.find((x) => d.reconocimiento === x.id), 'nombre'),
      Header: 'Tipo de reconocimiento'
    },      
  ]

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"interes"}
      />

  )
}


export default TableIntereses