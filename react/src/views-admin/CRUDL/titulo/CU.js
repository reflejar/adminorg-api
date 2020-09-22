import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { titulosActions } from '../../../redux/actions/titulos';
import { toastr } from "react-redux-toastr";

import Spinner from '../../../components/spinner/spinner';
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
        supertitulo: get(selected, 'supertitulo', ''),
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string().required(empty),
        numero: Yup.number().required(empty),
        supertitulo: Yup.number().required(empty),
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(titulosActions.send({ 
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
                <Field name="numero" id="numero" className={`form-control ${errors.numero && touched.numero && 'is-invalid'}`} />
                {errors.numero && touched.numero ? <div className="invalid-feedback">{errors.numero}</div> : null}
              </FormGroup>              
            </Col>
            <Col sm="6">
              <h4>Dependencia</h4>
              <FormGroup>
                <Label for="supertitulo">Rubro al que pertenece</Label>
                <Field component="select" name="supertitulo" id="supertitulo" className={`form-control ${errors.supertitulo && touched.supertitulo && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {titulos.filter(t => t.cuentas.length === 0).map((titulo, i) => {
                    return <option key={i} value={titulo.id}>{titulo.nombre}</option>
                  })}
                </Field>
                {errors.supertitulo && touched.supertitulo ? <div className="invalid-feedback">{errors.supertitulo}</div> : null}
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
