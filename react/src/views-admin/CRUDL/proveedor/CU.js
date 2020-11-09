import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { proveedoresActions } from '../../../redux/actions/proveedores';
import { toastr } from "react-redux-toastr";

import { Select } from '../../../components/Select';
import { mapToOptions } from '../../../utility/mappers';
import Spinner from '../../../components/spinner/spinner';
import { provincias } from '../../../utility/options/provincias';
import { tipo_documentos } from '../../../utility/options/documentos';
import { useRetenciones, useTitulos } from '../../../utility/hooks/dispatchers';

const empty = 'Campo requerido';

const filterAvailables = (arr) => arr.filter((x) => !x.cuenta_set.length > 0);

const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();
  const [retenciones, loadingRetenciones] = useRetenciones();
  const [titulos, loadingTitulos] = useTitulos();
  let retiene = [];
  let optionsRetiene = [];


  if (loadingTitulos || loadingRetenciones) {
    return (
      <div className="loading-modal">
        <br/><br/>
        <Spinner />
      </div>
    )
  }


  if (selected && selected.retiene){
    retiene = selected.retiene
        .map((val) => ({ value: val, label: get(retenciones.find(x => x.id === val), 'nombre') }));
    optionsRetiene = [
      ...mapToOptions(filterAvailables(retenciones)),
      ...mapToOptions(retenciones.filter((x) => x.inquilino === selected.id))
    ];
  } else {
    optionsRetiene = mapToOptions(filterAvailables(retenciones));
  }

  return (
    <Formik
      enableReinitialize
      initialValues={{
        nombre: get(selected, 'perfil.nombre', ''),
        apellido: get(selected, 'perfil.apellido', ''),
        razon_social: get(selected, 'perfil.razon_social', '') || '',
        tipo_documento: get(selected, 'perfil.tipo_documento', ''),
        numero_documento: get(selected, 'perfil.numero_documento', ''),
        fecha_nacimiento: get(selected, 'perfil.fecha_nacimiento', ''),
        es_extranjero: get(selected, 'perfil.es_extranjero', false),
        mail: get(selected, 'perfil.mail', ''),
        telefono: get(selected, 'perfil.telefono', ''),
        provincia: get(selected, 'perfil.domicilio.provincia', ''),
        localidad: get(selected, 'perfil.domicilio.localidad', ''),
        calle: get(selected, 'perfil.domicilio.calle', ''),
        numero: get(selected, 'perfil.domicilio.numero', ''),
        titulo: get(selected, 'titulo', ''),
        retiene
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string(),
        apellido: Yup.string(),
        razon_social: Yup.string().required(empty),
        tipo_documento: Yup.string().required(empty),
        numero_documento: Yup.number().required(empty),
        fecha_nacimiento: Yup.date().nullable(),
        es_extranjero: Yup.boolean(),
        mail: Yup.string().email("Email invalido").nullable(),
        telefono: Yup.string(),
        provincia: Yup.string(),
        localidad: Yup.string(),
        calle: Yup.string(),
        numero: Yup.string(),
        titulo: Yup.number().required(empty),
        retiene: Yup.array()        
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(proveedoresActions.send({ 
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
      // {({ errors, touched, handleSubmit, isSubmitting }) => (
        <Form onSubmit={handleSubmit}>
          <Row>
            <Col sm="6">
              <h4>Datos personales</h4>
              <FormGroup>
                <Label for="nombre">Nombre</Label>
                <Field name="nombre" id="nombre" className={`form-control ${errors.nombre && touched.nombre && 'is-invalid'}`} />
                {errors.nombre && touched.nombre ? <div className="invalid-feedback">{errors.nombre}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="apellido">Apellido</Label>
                <Field name="apellido" id="apellido" className={`form-control ${errors.apellido && touched.apellido && 'is-invalid'}`} />
                {errors.apellido && touched.apellido ? <div className="invalid-feedback">{errors.apellido}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="razon_social">Razon Social</Label>
                <Field name="razon_social" id="razon_social" className={`form-control ${errors.razon_social && touched.razon_social && 'is-invalid'}`} />
                {errors.razon_social && touched.razon_social ? <div className="invalid-feedback">{errors.razon_social}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="tipo_documento">Tipo de documento</Label>
                <Field component="select" name="tipo_documento" id="tipo_documento" className={`form-control ${errors.tipo_documento && touched.tipo_documento && 'is-invalid'}`}>
                  <option defaultValue={null}>---</option>
                  {tipo_documentos.map((documento, i) => (
                    <option key={i} value={documento}>{documento}</option>
                  ))}
                </Field>
                {errors.tipo_documento && touched.tipo_documento ? <div className="invalid-feedback">{errors.tipo_documento}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="numero_documento">Numero de documento</Label>
                <Field type="number" step="1" name="numero_documento" id="numero_documento" className={`form-control ${errors.numero_documento && touched.numero_documento && 'is-invalid'}`} />
                {errors.numero_documento && touched.numero_documento ? <div className="invalid-feedback">{errors.numero_documento}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="fecha_nacimiento">Fecha de Nacimiento</Label>
                <Field name="fecha_nacimiento" type="date" id="fecha_nacimiento" className={`form-control ${errors.fecha_nacimiento && touched.fecha_nacimiento && 'is-invalid'}`} />
                {errors.fecha_nacimiento && touched.fecha_nacimiento ? <div className="invalid-feedback">{errors.fecha_nacimiento}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="es_extranjero">Es extranjero?</Label>
                <Field type="checkbox" name="es_extranjero" id="es_extranjero" className={`form-control ${errors.es_extranjero && touched.es_extranjero && 'is-invalid'}`} />
                {errors.es_extranjero && touched.es_extranjero ? <div className="invalid-feedback">{errors.es_extranjero}</div> : null}
              </FormGroup>
            </Col>
            <Col sm="6">
              <h4>Otros datos</h4>
              <FormGroup>
                <Label for="mail">Direccion de email</Label>
                <Field name="mail" type="email" id="mail" className={`form-control ${errors.mail && touched.mail && 'is-invalid'}`} />
                {errors.mail && touched.mail ? <div className="invalid-feedback">{errors.mail}</div> : null}
              </FormGroup>

              <FormGroup>
                <Label for="telefono">Telefono</Label>
                <Field name="telefono" id="telefono" className={`form-control ${errors.telefono && touched.telefono && 'is-invalid'}`} />
                {errors.telefono && touched.telefono ? <div className="invalid-feedback">{errors.telefono}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="provincia">Provincia</Label>
                <Field component="select" name="provincia" id="provincia" className={`form-control ${errors.provincia && touched.provincia && 'is-invalid'}`}>
                  {provincias.map((provincia, i) => {
                    return <option key={i} value={provincia.id}>{provincia.nombre}</option>
                  })}
                </Field>
                {errors.provincia && touched.provincia ? <div className="invalid-feedback">{errors.provincia}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="localidad">Localidad</Label>
                <Field name="localidad" id="localidad" className={`form-control ${errors.localidad && touched.localidad && 'is-invalid'}`} />
                {errors.localidad && touched.localidad ? <div className="invalid-feedback">{errors.localidad}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="calle">Calle</Label>
                <Field name="calle" id="calle" className={`form-control ${errors.calle && touched.calle && 'is-invalid'}`} />
                {errors.calle && touched.calle ? <div className="invalid-feedback">{errors.calle}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="numero">Numero</Label>
                <Field name="numero" id="numero" className={`form-control ${errors.numero && touched.numero && 'is-invalid'}`} />
                {errors.numero && touched.numero ? <div className="invalid-feedback">{errors.numero}</div> : null}
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

            <Col xs={12}>
              <hr />
            </Col>

            <Col sm="6">


              <FormGroup>
                <Label for="retiene">Retiene</Label>
                <Select
                  isMulti
                  placeholder=""
                  name="retiene"
                  id="retiene"
                  className="basic-multi-select"
                  classNamePrefix="select"
                  error={errors.retiene && touched.retiene}
                  options={optionsRetiene}    
                  onChange={(option) => setFieldValue('retiene', option)}
                  value={values.retiene}
                />

                {errors.retiene && touched.retiene ? <div className="error-feedback">{errors.retiene}</div> : null}
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