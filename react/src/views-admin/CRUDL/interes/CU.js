import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { interesesActions } from '../../../redux/actions/intereses';
import { toastr } from "react-redux-toastr";
import { tipos, periodizaciones } from '../../../utility/options/metodos';

const empty = 'Campo requerido';


const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();

  return (
    <Formik
      enableReinitialize
      initialValues={{
        nombre: get(selected, 'nombre', ''),
        tipo: get(selected, 'tipo', ''),
        plazo: get(selected, 'plazo', ''),
        monto: get(selected, 'monto', ''),
        reconocimiento: get(selected, 'reconocimiento', ''),
        base_calculo: get(selected, 'base_calculo', ''),
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string().required(empty),
        tipo: Yup.string().required(empty),
        plazo: Yup.number().required(empty),
        monto: Yup.number().required(empty),
        reconocimiento: Yup.number(),
        base_calculo: Yup.number(),
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(interesesActions.send({ 
            ...values, 
            id: get(selected, 'id', null) 
          })).then(() => {
            toastr.success('¡Listo! Guardado con éxito');
          });
          if (onClose) {
            onClose(false);
          }
        } catch (error) {
          console.error(error);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ errors, touched, handleSubmit, isSubmitting }) => (
        <Form onSubmit={handleSubmit}>
          <Row>
            <Col sm="6">
              <h4>Datos Principales</h4>
              <FormGroup>
                <Label for="nombre">Nombre</Label>
                <Field name="nombre" id="nombre" className={`form-control ${errors.nombre && touched.nombre && 'is-invalid'}`} />
                {errors.nombre && touched.nombre ? <div className="invalid-feedback">{errors.nombre}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="plazo">Plazo</Label>
                <Field type="number" step="1" name="plazo" id="plazo" className={`form-control ${errors.plazo && touched.plazo && 'is-invalid'}`} />
                {errors.plazo && touched.plazo ? <div className="invalid-feedback">{errors.plazo}</div> : null}
              </FormGroup>                  
              <FormGroup>
                <Label for="tipo">Tipo de interes</Label>
                <Field component="select" name="tipo" id="tipo" className={`form-control ${errors.tipo && touched.tipo && 'is-invalid'}`}>
                  {tipos.map((tipo, i) => {
                    return <option key={i} value={tipo.id}>{tipo.nombre}</option>
                  })}
                </Field>
                {errors.tipo && touched.tipo ? <div className="invalid-feedback">{errors.tipo}</div> : null}
              </FormGroup>                           
            </Col>
            <Col sm="6">
              <h4>Datos Principales</h4>
              <FormGroup>
                <Label for="monto">Monto</Label>
                <Field type="number" step="0.01" name="monto" id="monto" className={`form-control ${errors.monto && touched.monto && 'is-invalid'}`} />
                {errors.monto && touched.monto ? <div className="invalid-feedback">{errors.monto}</div> : null}
              </FormGroup>              
              <FormGroup>
                <Label for="base_calculo">Base de calculo</Label>
                <Field component="select" name="base_calculo" id="base_calculo" className={`form-control ${errors.base_calculo && touched.base_calculo && 'is-invalid'}`}>
                  {periodizaciones.map((periodo, i) => {
                    return <option key={i} value={periodo.id}>{periodo.nombre}</option>
                  })}
                </Field>
                {errors.base_calculo && touched.base_calculo ? <div className="invalid-feedback">{errors.base_calculo}</div> : null}
              </FormGroup>              
              <FormGroup>
                <Label for="reconocimiento">Reconocimiento</Label>
                <Field component="select" name="reconocimiento" id="reconocimiento" className={`form-control ${errors.reconocimiento && touched.reconocimiento && 'is-invalid'}`}>
                  {periodizaciones.map((periodo, i) => {
                    return <option key={i} value={periodo.id}>{periodo.nombre}</option>
                  })}
                </Field>
                {errors.reconocimiento && touched.reconocimiento ? <div className="invalid-feedback">{errors.reconocimiento}</div> : null}
              </FormGroup>
            </Col>

            <Col xs={12}>
              <hr />
            </Col>


          </Row>

          <Button type="submit" color="primary" className="button-clip-loader" disabled={isSubmitting}>
            {isSubmitting && (
              <ClipLoader
                sizeUnit="px"
                size={18}
                color="#FF586B"
              />
            )}

            Guardar
          </Button>
        </Form>
      )}
    </Formik>
  );
};

export default CU;