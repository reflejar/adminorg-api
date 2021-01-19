import React from "react";

import { useTitulos } from '../../../../utility/hooks/dispatchers';
import Table from "./editSelectTable";
import get from 'lodash/get';
import Spinner from "../../../../components/spinner/spinner";
import { naturalezas } from '../../../CRUDL/titulo/_options';


const TableTitulos = ({toggle, setItem}) => {

  const [items, loadingItems] = useTitulos();
  
  const titles = [
    {
      accessor: 'numero',
      Header: 'Numero'
    },
    {
      accessor: 'nombre',
      Header: 'Nombre'
    },
    {
      id: 'Rubro',
      accessor: (d) => get(items.find((x) => d.supertitulo === x.id), 'full_name', 'S/R'),
      Header: 'Rubro'
    },  
    {
      id: 'Predeterminado para',
      accessor: (d) => get(naturalezas.find((x) => d.predeterminado === x.id), 'nombre', ''),
      Header: 'Predeterminado para'
    },  
  ]

  if (loadingItems) {
    return <Spinner />
  }

  return (
    <div>
      <Table
        titles={titles}
        items={items}
        loadingItems={loadingItems}
        toggle={toggle}
        selectItem={setItem}
        causante={"titulo"}
      />

    </div>

)
}

export default TableTitulos;
