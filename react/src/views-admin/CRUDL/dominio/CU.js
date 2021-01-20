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
import { useTitulos, useClientes } from '../../../utility/hooks/dispatchers';

const empty = 'Campo requerido';

const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();

  const [titulos, loadingTitulos] = useTitulos();
  const [clientes, loadingClientes] = useClientes();

  if (loadingTitulos || loadingClientes) {
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
        propietario: get(selected, 'propietario', ''),
        inquilino: get(selected, 'inquilino', ''),
        domicilio_superficie_total: get(selected, 'domicilio.superficie_total', ''),
        domicilio_superficie_cubierta: get(selected, 'domicilio.superficie_cubierta', ''),
        titulo: get(selected, 'titulo', ''),
        domicilio_provincia: get(selected, 'domicilio.provincia', ''),
        domicilio_localidad: get(selected, 'domicilio.localidad', ''),
        domicilio_calle: get(selected, 'domicilio.calle', ''),
        domicilio_numero: get(selected, 'domicilio.numero', ''),
        domicilio_piso: get(selected, 'domicilio.piso', ''),
        domicilio_manzana: get(selected, 'domicilio.manzana', ''),
        domicilio_oficina: get(selected, 'domicilio.oficina', ''),
        domicilio_sector: get(selected, 'domicilio.sector', ''),
        domicilio_torre: get(selected, 'domicilio.torre', ''),
        domicilio_parcela: get(selected, 'domicilio.parcela', ''),
        domicilio_catastro: get(selected, 'domicilio.catastro', ''),
      }}
      validationSchema={Yup.object().shape({
        numero: Yup.number().required(empty),
        propietario: Yup.number().required(empty),
        inquilino: Yup.number().required(empty),
        domicilio_superficie_total: Yup.number().nullable(true),
        domicilio_superficie_cubierta: Yup.number().nullable(true),
        titulo: Yup.number().required(empty),
        domicilio_provincia: Yup.string(),
        domicilio_localidad: Yup.string(),
        domicilio_calle: Yup.string(),
        domicilio_numero: Yup.string(),
        domicilio_piso: Yup.string().nullable(true),
        domicilio_manzana: Yup.string().nullable(true),
        domicilio_oficina: Yup.string().nullable(true),
        domicilio_sector: Yup.string().nullable(true),
        domicilio_torre: Yup.string().nullable(true),
        domicilio_parcela: Yup.string().nullable(true),
        domicilio_catastro: Yup.string().nullable(true),
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
                <Label for="numero">Identificacion</Label>
                <Field type="number" step="1" name="numero" id="numero" className={`form-control ${errors.numero && touched.numero && 'is-invalid'}`} />
                {errors.numero && touched.numero ? <div className="invalid-feedback">{errors.numero}</div> : null}
              </FormGroup>    

              <FormGroup>
                <Label for="propietario">Propietario</Label>
                <Field component="select" name="propietario" id="propietario" className={`form-control ${errors.propietario && touched.propietario && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {clientes.map((cliente, i) => {
                    return <option key={i} value={cliente.id}>{cliente.full_name}</option>
                  })}
                </Field>
                {errors.propietario && touched.propietario ? <div className="invalid-feedback">{errors.propietario}</div> : null}
              </FormGroup>

              <FormGroup>
                <Label for="inquilino">Inquilino</Label>
                <Field component="select" name="inquilino" id="inquilino" className={`form-control ${errors.inquilino && touched.inquilino && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {clientes.map((cliente, i) => {
                    return <option key={i} value={cliente.id}>{cliente.full_name}</option>
                  })}
                </Field>
                {errors.inquilino && touched.inquilino ? <div className="invalid-feedback">{errors.inquilino}</div> : null}
              </FormGroup>    

              <FormGroup>
                <Label for="domicilio_superficie_total">Superficie Total</Label>
                <Field type="number" step="0.01" name="domicilio_superficie_total" id="domicilio_superficie_total" className={`form-control ${errors.domicilio_superficie_total && touched.domicilio_superficie_total && 'is-invalid'}`} />
                {errors.domicilio_superficie_total && touched.domicilio_superficie_total ? <div className="invalid-feedback">{errors.domicilio_superficie_total}</div> : null}
              </FormGroup>

              <FormGroup>
                <Label for="domicilio_superficie_cubierta">Superficie Cubierta</Label>
                <Field type="number" step="0.01" name="domicilio_superficie_cubierta" id="domicilio_superficie_cubierta" className={`form-control ${errors.domicilio_superficie_cubierta && touched.domicilio_superficie_cubierta && 'is-invalid'}`} />
                {errors.domicilio_superficie_cubierta && touched.domicilio_superficie_cubierta ? <div className="invalid-feedback">{errors.domicilio_superficie_cubierta}</div> : null}
              </FormGroup>    

              <FormGroup>
                <Label for="titulo">Titulo contable</Label>
                <Field component="select" name="titulo" id="titulo" className={`form-control ${errors.titulo && touched.titulo && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {titulos.map((titulo, i) => {
                    return <option key={i} value={titulo.id}>{titulo.nombre}</option>
                  })}
                </Field>
                {errors.titulo && touched.titulo ? <div className="invalid-feedback">{errors.titulo}</div> : null}
              </FormGroup>              
            </Col>
            <Col sm="6">
              <h4>Datos del domicilio</h4>
                <Row>
                  <Col sm="6">
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
                      <Label for="domicilio_manzana">Manzana</Label>
                      <Field name="domicilio_manzana" id="domicilio_manzana" className={`form-control ${errors.domicilio_manzana && touched.domicilio_manzana && 'is-invalid'}`} />
                      {errors.domicilio_manzana && touched.domicilio_manzana ? <div className="invalid-feedback">{errors.domicilio_manzana}</div> : null}
                    </FormGroup>
                    <FormGroup>
                      <Label for="domicilio_torre">Torre</Label>
                      <Field name="domicilio_torre" id="domicilio_torre" className={`form-control ${errors.domicilio_torre && touched.domicilio_torre && 'is-invalid'}`} />
                      {errors.domicilio_torre && touched.domicilio_torre ? <div className="invalid-feedback">{errors.domicilio_torre}</div> : null}
                    </FormGroup>   
                    <FormGroup>
                      <Label for="domicilio_catastro">Catastro</Label>
                      <Field name="domicilio_catastro" id="domicilio_catastro" className={`form-control ${errors.domicilio_catastro && touched.domicilio_catastro && 'is-invalid'}`} />
                      {errors.domicilio_catastro && touched.domicilio_catastro ? <div className="invalid-feedback">{errors.domicilio_catastro}</div> : null}
                    </FormGroup>                                          
                  </Col>
                  <Col sm="6">
                    <FormGroup>
                      <Label for="domicilio_localidad">Localidad</Label>
                      <Field name="domicilio_localidad" id="domicilio_localidad" className={`form-control ${errors.domicilio_localidad && touched.domicilio_localidad && 'is-invalid'}`} />
                      {errors.domicilio_localidad && touched.domicilio_localidad ? <div className="invalid-feedback">{errors.domicilio_localidad}</div> : null}
                    </FormGroup>                    
                    <FormGroup>
                      <Label for="domicilio_piso">Piso</Label>
                      <Field name="domicilio_piso" id="domicilio_piso" className={`form-control ${errors.domicilio_piso && touched.domicilio_piso && 'is-invalid'}`} />
                      {errors.domicilio_piso && touched.domicilio_piso ? <div className="invalid-feedback">{errors.domicilio_piso}</div> : null}
                    </FormGroup>
                    <FormGroup>
                      <Label for="domicilio_sector">Sector</Label>
                      <Field name="domicilio_sector" id="domicilio_sector" className={`form-control ${errors.domicilio_sector && touched.domicilio_sector && 'is-invalid'}`} />
                      {errors.domicilio_sector && touched.domicilio_sector ? <div className="invalid-feedback">{errors.domicilio_sector}</div> : null}
                    </FormGroup>      
                    <FormGroup>
                      <Label for="domicilio_oficina">Oficina</Label>
                      <Field name="domicilio_oficina" id="domicilio_oficina" className={`form-control ${errors.domicilio_oficina && touched.domicilio_oficina && 'is-invalid'}`} />
                      {errors.domicilio_oficina && touched.domicilio_oficina ? <div className="invalid-feedback">{errors.domicilio_oficina}</div> : null}
                    </FormGroup>              
                    <FormGroup>
                      <Label for="domicilio_parcela">Parcela</Label>
                      <Field name="domicilio_parcela" id="domicilio_parcela" className={`form-control ${errors.domicilio_parcela && touched.domicilio_parcela && 'is-invalid'}`} />
                      {errors.domicilio_parcela && touched.domicilio_parcela ? <div className="invalid-feedback">{errors.domicilio_parcela}</div> : null}
                    </FormGroup>



                  </Col>
                </Row>
         

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
