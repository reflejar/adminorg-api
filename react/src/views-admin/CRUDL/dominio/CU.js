import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { dominiosActions } from '../../../redux/actions/dominios';
import { toastr } from "react-redux-toastr";

import Spinner from '../../../components/spinner/spinner';
import { provincias } from '../../../utility/options/provincias';
import { useTitulos } from '../../../utility/hooks/dispatchers';

const empty = 'Campo requerido';

const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();

  const [titulos, loadingTitulos] = useTitulos();

  if (loadingTitulos) {
    return (
      <div className="loading-modal">
        <br/><br/>
        <Spinner />
      </div>
    )
  }

  return (
    <Formik
      enableReinitialize
      initialValues={{
        nombre: get(selected, 'nombre', ''),
        numero: get(selected, 'numero', ''),
        domicilio_provincia: get(selected, 'domicilio.provincia', ''),
        domicilio_localidad: get(selected, 'domicilio.localidad', ''),
        domicilio_calle: get(selected, 'domicilio.calle', ''),
        domicilio_numero: get(selected, 'domicilio.numero', ''),
        titulo: get(selected, 'titulo', ''),
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string().required(empty),
        numero: Yup.number().required(empty),
        domicilio_provincia: Yup.string(),
        domicilio_localidad: Yup.string(),
        domicilio_calle: Yup.string(),
        domicilio_numero: Yup.string(),
        titulo: Yup.number().required(empty),
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(dominiosActions.send({ 
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
      {({ errors, touched, setFieldValue, handleSubmit, isSubmitting, values }) => (
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
                <Label for="numero">Numero</Label>
                <Field type="number" step="1" name="numero" id="numero" className={`form-control ${errors.numero && touched.numero && 'is-invalid'}`} />
                {errors.numero && touched.numero ? <div className="invalid-feedback">{errors.numero}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="domicilio_provincia">Provincia</Label>
                <Field component="select" name="domicilio_provincia" id="domicilio_provincia" className={`form-control ${errors.domicilio_provincia && touched.domicilio_provincia && 'is-invalid'}`}>
                  {provincias.map((domicilio_provincia, i) => {
                    return <option key={i} value={domicilio_provincia.id}>{domicilio_provincia.nombre}</option>
                  })}
                </Field>
                {errors.domicilio_provincia && touched.domicilio_provincia ? <div className="invalid-feedback">{errors.domicilio_provincia}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="domicilio_localidad">Localidad</Label>
                <Field name="domicilio_localidad" id="domicilio_localidad" className={`form-control ${errors.domicilio_localidad && touched.domicilio_localidad && 'is-invalid'}`} />
                {errors.domicilio_localidad && touched.domicilio_localidad ? <div className="invalid-feedback">{errors.domicilio_localidad}</div> : null}
              </FormGroup>
            </Col>
            <Col sm="6">
              <h4>Otros datos</h4>
              <FormGroup>
                <Label for="domicilio_calle">Calle</Label>
                <Field name="domicilio_calle" id="domicilio_calle" className={`form-control ${errors.domicilio_calle && touched.domicilio_calle && 'is-invalid'}`} />
                {errors.domicilio_calle && touched.domicilio_calle ? <div className="invalid-feedback">{errors.domicilio_calle}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="domicilio_numero">Numero</Label>
                <Field name="domicilio_numero" id="domicilio_numero" className={`form-control ${errors.domicilio_numero && touched.domicilio_numero && 'is-invalid'}`} />
                {errors.domicilio_numero && touched.domicilio_numero ? <div className="invalid-feedback">{errors.domicilio_numero}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="titulo">Cuenta contable</Label>
                <Field component="select" name="titulo" id="titulo" className={`form-control ${errors.titulo && touched.titulo && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {titulos.map((titulo, i) => {
                    return <option key={i} value={titulo.id}>{titulo.nombre}</option>
                  })}
                </Field>
                {errors.titulo && touched.titulo ? <div className="invalid-feedback">{errors.titulo}</div> : null}
              </FormGroup>
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
