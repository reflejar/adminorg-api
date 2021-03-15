import React, {Fragment} from "react";

import { Row, Col, Table } from "reactstrap";


const Sumas = () => {

  return (
    <Fragment>
      <Row>
        <Col sm="12">
          Las sumitas. 
          Tiene que tener input para los conceptos a sumar (Cuentas (seleccionando naturaleza) o titulos)
          Tiene que tener input para las columnas sumantes (valor; o debe y haber; o debe, haber y valor;)
            Y tiene que haber tantas columnas sumantes como las seleccionadas * la cantidad de periodos consultados
              Por ejemplo: Seleccionando columnas debe + haber + valor (3 columnas) y seleccionamos 2 periodos diferentes => 6 columnas
          Tiene que tener input para filtrado/agrupado (por ej: conceptos a sumar: Cuentas - agrupado: conceptos y periodos)
        </Col>
      </Row>
      <Row>
        <Col sm="12">
          <Table responsive>
              <thead>
                <tr>
                  <th>Concepto</th>
                  <th>Suma</th>
                  <th>%</th>
                </tr>
              </thead>          
              <tbody>
                
              </tbody>

          </Table>
        </Col>
      </Row>
    </Fragment>
  );
}

export default Sumas;



