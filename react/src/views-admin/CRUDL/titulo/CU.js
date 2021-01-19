import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { titulosActions } from '../../../redux/actions/titulos';
import { toastr } from "react-redux-toastr";
import { naturalezas } from './_options';

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
        numero: get(selected, 'numero', ''),
        nombre: get(selected, 'nombre', ''),
        predeterminado: get(selected, 'predeterminado', ''),
        supertitulo: get(selected, 'supertitulo', ''),
      }}
      validationSchema={Yup.object().shape({
        numero: Yup.number().required(empty),
        nombre: Yup.string().required(empty),
        predeterminado: Yup.string(),
        supertitulo: Yup.number().nullable(true),
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
              <FormGroup>
                <Label for="predeterminado">Titulo predeterminado para</Label>
                <Field component="select" name="predeterminado" id="predeterminado" className={`form-control ${errors.predeterminado && touched.predeterminado && 'is-invalid'}`}>
                  <option value=""> --- </option>
                  {naturalezas.map((n, i) => {
                    return <option key={i} value={n.id}>{n.nombre}</option>
                  })}
                </Field>
                {errors.predeterminado && touched.predeterminado ? <div className="invalid-feedback">{errors.predeterminado}</div> : null}
              </FormGroup>                   
            </Col>
            <Col sm="6">
              <h4>Dependencia</h4>
              <FormGroup>
                <Label for="supertitulo">Rubro al que pertenece</Label>
                <Field component="select" name="supertitulo" id="supertitulo" className={`form-control ${errors.supertitulo && touched.supertitulo && 'is-invalid'}`}>
                  <option value=""> --- </option>
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
