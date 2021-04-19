import React, { Component, Fragment } from "react";

import { Row, Col, Card, CardBody, CardTitle } from 'reactstrap';


class FAQ extends Component {

  render() {
    return (
      <Fragment>
        <Row className="row-eq-height">
          <Col md="12">
            <Card>
              <CardBody>
                <CardTitle>FAQ</CardTitle>

              </CardBody>
            </Card>               
          </Col>       
        </Row>   
      </Fragment>
    );
  }
}

export default FAQ;
