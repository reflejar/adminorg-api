import React, {Fragment} from "react";

import { Row, Col, Table } from "reactstrap";


const Sumas = () => {

  return (
    <Fragment>
      <Row>
        <Col sm="12">
          Las sumitas
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



