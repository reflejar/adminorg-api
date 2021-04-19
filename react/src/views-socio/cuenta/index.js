import React, { Component, Fragment } from "react";
import Cuenta from "../../components/board/content/cuenta";
import CuentaTable from "./table";
import { connect } from 'react-redux';
import { Row, Col, Card, CardBody, CardTitle } from 'reactstrap';

// Styling

class CuentaSocio extends Component {
   render() {
      const {cuenta_id} = this.props 
      const cuenta = {id:cuenta_id}
      return (
         <Fragment>
            <Row className="row-eq-height">
            <Col md="12">
               <Card>
                  <CardBody>
                     <CardTitle>Mis movimientos</CardTitle>
                     <div className="text-center">
                        <Cuenta selected={cuenta} Table={CuentaTable}/>
                     </div>
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

export default connect(mapStateToProps, null)(CuentaSocio);