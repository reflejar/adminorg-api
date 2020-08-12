import React from "react";

import { useDominios, useClientes } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable";
import get from 'lodash/get';


const TableDominio = ({toggle, setItem}) => {
  
  const [clientes] = useClientes();

  const [items, loadingItems] = useDominios();
  
  const titles = [
    {
      accessor: 'nombre',
      Header: 'Nombre'
    },
    {
      accessor: 'numero',
      Header: 'Numero'
    },
    {
      id: 'Propietario',
      accessor: (d) => get(clientes.find((x) => d.propietario === x.id), 'full_name', 'S/P'),
      Header: 'Propietario'
    },  
    {
      id: 'Ocupante',
      accessor: (d) => get(clientes.find((x) => d.ocupante === x.id), 'full_name', 'S/O'),
      Header: 'Ocupante'
    },  
  ]

  return (
    <div>
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"dominio"}
      />

    </div>

)
}

export default TableDominio;
