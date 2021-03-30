import React, { Component, Fragment } from "react";
// import Deuda from "../../views-admin/clientes/containers/content/deudas";
import { Row, Col, Card, CardBody, CardTitle } from 'reactstrap';

// Styling

class Deudas extends Component {
   render() {
      return (
         <Fragment>
            <Row className="row-eq-height">
            <Col md="12">
               <Card>
                  <CardBody>
                     <CardTitle>Mis deudas</CardTitle>
                     {/* <Deuda /> */}
                  </CardBody>
               </Card>               
            </Col>       
            </Row>
         </Fragment>
      );
   }
}

export default Deudas;
