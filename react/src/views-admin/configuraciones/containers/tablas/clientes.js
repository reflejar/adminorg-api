import React from "react";

import { useClientes } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"


const TableCliente = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useClientes();

  const titles = [
    {
      accessor: 'full_name',
      Header: 'Nombre'
    },
    {
      accessor: 'perfil.numero_documento',
      Header: 'Documento'
    },
    {
      accessor: 'perfil.mail',
      Header: 'Email'
    },  
    {
      accessor: 'perfil.telefono',
      Header: 'Telefono'
    }  
  ]  

  return (
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"cliente"}
      />

  )
}


export default TableCliente
