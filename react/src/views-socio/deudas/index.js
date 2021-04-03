import React, { Component, Fragment } from "react";
import Deudas from "../../components/board/content/deudas";
import DeudasTable from "./table";
import { connect } from 'react-redux';
import { Row, Col, Card, CardBody, CardTitle } from 'reactstrap';

// Styling

class DeudasSocio extends Component {
   render() {
      const {cuenta_id} = this.props 
      const cuenta = {id:cuenta_id}
      return (
         <Fragment>
            <Row className="row-eq-height">
            <Col md="12">
               <Card>
                  <CardBody>
                     <CardTitle>Mis deudas</CardTitle>
                     <Deudas selected={cuenta} Table={DeudasTable}/>
                  </CardBody>
               </Card>               
            </Col>       
            </Row>
         </Fragment>
      );
   }
}

const mapStateToProps = (state) => ({
   cuenta_id: state.user.auth.profile.cuenta,
});

export default connect(mapStateToProps, null)(DeudasSocio);