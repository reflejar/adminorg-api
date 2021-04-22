import React from "react";
import { Table } from 'reactstrap';
import { useCarpetas } from "../../../utility/hooks/dispatchers";
import Item from './item'

import Spinner from "../../../components/spinner/spinner";

const fitlerParents = (arr) => arr.filter(x => !x.supercarpeta);
const filterChildren = (arr, item) => arr.filter(x => x.supercarpeta === item.id);


const List = ({selected}) => {
    
    const [carpetas, loadingTitulos] = useCarpetas(true);

    if (loadingTitulos) {
        return <Spinner />
      }
  

    return (
        <div className="list-group position-relative" id="users-list">
          <div className="users-list-padding">
          <Table size="sm" responsive>
               <thead>
                  <tr>
                     <th>Carpetas y archivos</th>
                  </tr>
               </thead>
               <tbody>
                {carpetas && fitlerParents(carpetas).map((item, key) => (
                <Item 
                    indentation={0}
                    item={item} 
                    key={key}
                    children={filterChildren(carpetas, item)}
                    carpetas={carpetas}
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