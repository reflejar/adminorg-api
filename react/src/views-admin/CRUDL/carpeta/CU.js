import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { carpetasActions } from '../../../redux/actions/carpetas';
import { toastr } from "react-redux-toastr";
import { Select } from '../../../components/Select';

import Spinner from '../../../components/spinner/spinner';
import { useCarpetas } from '../../../utility/hooks/dispatchers';

const empty = 'Campo requerido';

const excludeInstance = (selected, arr) =>
  arr.filter((x) => selected ? x.id !== selected.id : x);

const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();

  const [carpetas, loadingCarpetas] = useCarpetas();

  const optionsExposicion = [{
    label: "Administrativos",
    value: "administrativo",
  },{
    label: "Socios",
    value: "socio",
  }];


  if (loadingCarpetas) {
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
        descripcion: get(selected, 'descripcion', ''),
        supercarpeta: get(selected, 'supercarpeta', ''),
        exposicion: get(selected, 'exposicion', ''),
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string().required(empty),
        descripcion: Yup.string(),
        supercarpeta: Yup.number(),
        exposicion: Yup.array(),
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(carpetasActions.send({ 
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
            <Col sm="12">
              <h4>Datos Principales</h4>
              <FormGroup>
                <Label for="nombre">Nombre</Label>
                <Field name="nombre" id="nombre" className={`form-control ${errors.nombre && touched.nombre && 'is-invalid'}`} />
                {errors.nombre && touched.nombre ? <div className="invalid-feedback">{errors.nombre}</div> : null}
              </FormGroup>
              <FormGroup>
                <Label for="descripcion">Descripcion</Label>
                <Field name="descripcion" id="descripcion" className={`form-control ${errors.descripcion && touched.descripcion && 'is-invalid'}`} />
                {errors.descripcion && touched.descripcion ? <div className="invalid-feedback">{errors.descripcion}</div> : null}
              </FormGroup>              
              <FormGroup>
                <Label for="exposicion">Exponer a grupo:</Label>
                  <Select
                    isMulti
                    placeholder=""
                    name="exposicion"
                    id="exposicion"
                    className="basic-multi-select"
                    classNamePrefix="select"
                    error={errors.exposicion && touched.exposicion}
                    options={optionsExposicion}    
                    onChange={(options) => setFieldValue('exposicion', options)}
                    value={values.exposicion}
                  />

                {errors.exposicion && touched.exposicion ? <div className="error-feedback">{errors.exposicion}</div> : null}
              </FormGroup>     
              <FormGroup>
                <Label for="supercarpeta">Colocar dentro de otra carpeta</Label>
                <Field component="select" name="supercarpeta" id="supercarpeta" className={`form-control ${errors.supercarpeta && touched.supercarpeta && 'is-invalid'}`}>
                  <option value={""}> --- </option>
                  {excludeInstance(selected, carpetas).map((carpeta, i) => {
                    return <option key={i} value={carpeta.id}>{carpeta.nombre}</option>
                  })}
                </Field>
                {errors.supercarpeta && touched.supercarpeta ? <div className="invalid-feedback">{errors.supercarpeta}</div> : null}
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
