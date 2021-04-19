import React, { Component, Fragment } from "react";

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
                     <CardTitle>Informes</CardTitle>

                     <p>Aun no tenemos reportes para mostrarte</p>
                  </CardBody>
               </Card>               
            </Col>       
            </Row>           
         </Fragment>
      );
   }
}

export default Deudas;
