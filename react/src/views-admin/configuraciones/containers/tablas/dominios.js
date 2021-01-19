import React from "react";

import { useDominios, useClientes } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable";
import get from 'lodash/get';
import Spinner from "../../../../components/spinner/spinner";

const TableDominio = ({toggle, setItem}) => {
  
  const [clientes, loadingClientes] = useClientes();

  const [items, loadingItems] = useDominios();
  
  const titles = [
    {
      accessor: 'numero',
      Header: 'Identificacion'
    },
    {
      id: 'Propietario',
      accessor: (d) => get(clientes.find((x) => d.propietario === x.id), 'full_name', 'S/P'),
      Header: 'Propietario'
    },  
    {
      id: 'Inquilino',
      accessor: (d) => get(clientes.find((x) => d.inquilino === x.id), 'full_name', 'S/O'),
      Header: 'Inquilino'
    },  
  ]

  if (loadingClientes) {
    return <Spinner />
  }

  return (
    <div>
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems || loadingClientes}
        toggle={toggle}
        selectItem={setItem}
        causante={"dominio"}
      />

    </div>

)
}

export default TableDominio;
