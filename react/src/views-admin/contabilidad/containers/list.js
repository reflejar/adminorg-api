import React from "react";
import { Table } from 'reactstrap';
import { useTitulos } from "../../../utility/hooks/dispatchers";
import Item from './item'

import Spinner from "../../../components/spinner/spinner";

const fitlerParents = (arr) => arr.filter(x => !x.supertitulo);
const filterChildren = (arr, item) => arr.filter(x => x.supertitulo === item.id);


const List = ({selected}) => {
    
    const [titulos, loadingTitulos] = useTitulos(true);


    if (loadingTitulos) {
        return <Spinner />
      }
  

    return (
        <div className="list-group position-relative" id="users-list">
          <div className="users-list-padding">
          <Table size="sm" responsive borderless={true} hover={true}>
               <thead>
                  <tr>
                     <th>Titulo/Cuenta</th>
                     <th className="text-right">N°</th>
                  </tr>
               </thead>
               <tbody>
                {titulos && fitlerParents(titulos).map((item, key) => (
                <Item 
                    indentation={0}
                    item={item}
                    key={key} 
                    children={filterChildren(titulos, item)}
                    titulos={titulos}
                    filterChildren={filterChildren}
                    selected={selected}
                />))}

               </tbody>
            </Table>
          </div>
        </div>
      );

}

export default List