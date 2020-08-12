import React from "react";

import { useProveedores } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable"


const TableProveedor = ({toggle, setItem}) => {
  
  const [items, loadingItems] = useProveedores();

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
        causante={"proveedor"}
      />

  )
}


export default TableProveedor
