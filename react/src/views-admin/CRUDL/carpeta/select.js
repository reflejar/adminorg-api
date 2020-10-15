import React, { Component, Fragment } from "react";
import { Row, Col, Button, FormGroup, Label } from "reactstrap";
import { Formik, Field, Form } from "formik";
import * as Yup from "yup";
import { connect } from 'react-redux';

import { titulosActions } from '../../../redux/actions/titulos';

const empty = "Campo requerido";

const formSchema = Yup.object().shape({
  nombre: Yup.string().required(empty),
});

class CRUDL extends Component {

  async componentWillMount() {
    if (!this.props.titulos) {
      await this.props.getTitulos();
    }
  }

  render() {
    return (
      <Fragment>
        <Formik
          initialValues={{
            nombre: "",
          }}
          validationSchema={formSchema}
          onSubmit={values => {
            // same shape as initial values
            console.log(values);
          }}
        >
          {({ errors, touched }) => (
            <Form>
            <Row>
              <Col sm="6">
                <h4>Datos personales</h4>
                <FormGroup>
                  <Label for="nombre">Nombre</Label>
                  <Field name="nombre" id="nombre" className={`form-control ${errors.nombre && touched.nombre && 'is-invalid'}`} />
                  {errors.nombre && touched.nombre ? <div className="invalid-feedback">{errors.nombre}</div> : null}
                </FormGroup>
              </Col>
            </Row>
            {
              this.props.submit
              ? <Row><Col sm="12"><Button type="submit" color="info" className="pull-right">Guardar</Button></Col></Row>
              : ""
            }
            </Form>
          )}
        </Formik>
      </Fragment>
    );
  }
}
const mapStateToProps = (state) => ({
  titulos: state.titulos.list,
});

const mapDispatchToProps = dispatch => ({
  getTitulos: () => dispatch(titulosActions.get())
})

export default connect(mapStateToProps, mapDispatchToProps)(CRUDL);