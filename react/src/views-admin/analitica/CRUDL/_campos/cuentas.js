import React, { useEffect } from 'react';
import { Row, Col, Table } from "reactstrap";
import Item from "../../../contabilidad/containers/item"
import { useTitulos } from "../../../../utility/hooks/dispatchers";

// Components
import { AppendableRowField } from '../../../../components/form/AppendableRowField';

import { useAppendableField } from '../../../../components/form/hooks';

// const basicErrorMessage = "La suma de los montos a perdonar deben ser estrictamente iguales al la suma del los montos de cada portador.";

const fitlerParents = (arr) => arr.filter(x => !x.supertitulo);
const filterChildren = (arr, item) => arr.filter(x => x.supertitulo === item.id);

  

const Cuentas = ({ filtro, setFiltro }) => {
  
  const [titulos, loadingTitulos] = useTitulos(true);


  // useEffect(() => {
  //   const updatedCuentas = filterCompletedObject(fechas);
  //   setFiltro((state) => ({
  //     ...state,
  //     fechas: updatedCuentas
  //   }));
  // }, [fechas, setFiltro])

  return (
    <Row>
      <Col sm="12">
        <Table size="sm" responsive>
          <thead>
            <tr>
                <th>Titulo/Cuenta</th>
                <th className="text-right">N°</th>
            </tr>
          </thead>
          <tbody>
          {titulos && fitlerParents(titulos).map(item => (
          <Item 
              indentation={0}
              item={item} 
              children={filterChildren(titulos, item)}
              titulos={titulos}
              filterChildren={filterChildren}
          />))}

          </tbody>
      </Table>
      </Col>
    </Row>
  );
};


export default Cuentas;