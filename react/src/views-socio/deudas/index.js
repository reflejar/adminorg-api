import React, { Component, Fragment } from "react";
// import Deuda from "../../views-admin/clientes/containers/content/deudas";
import { Row, Col, Card, CardBody, CardTitle } from 'reactstrap';

// Styling

class Deudas extends Component {
   render() {
      return (
         <Fragment>
            <Row className="row-eq-height">
            <Col md="9">
               <Card>
                  <CardBody>
                     <CardTitle>Estado de deudas</CardTitle>
                     {/* <Deuda /> */}
                  </CardBody>
               </Card>               
            </Col>
            <Col md="3">
               <Card>
                  <CardBody>
                     <CardTitle>MercadoPago</CardTitle>
                     <p>
                        Aqui podes aumentar tu saldo realizando un pago a MercadoPago.
                     </p>
                  </CardBody>                  
               </Card>
            </Col>            
            </Row>
         </Fragment>
      );
   }
}

export default Deudas;
