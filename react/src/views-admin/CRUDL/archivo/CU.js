import React from 'react';
import { Row, Col, FormGroup, Label, Button } from 'reactstrap';
import { Formik, Field, Form } from "formik";
import * as Yup from 'yup';
import { ClipLoader } from 'react-spinners';
import get from 'lodash/get';
import { useDispatch } from 'react-redux';
import { archivosActions } from '../../../redux/actions/archivos';
import { toastr } from "react-redux-toastr";
//import {ImportFileDropzone} from '../../../components/dropzone/ImportFileDropzone';

import Spinner from '../../../components/spinner/spinner';
import { useCarpetas } from '../../../utility/hooks/dispatchers';

const empty = 'Campo requerido';

const CU = ({ selected, onClose }) => {
  const dispatch = useDispatch();

  const [carpetas, loadingCarpetas] = useCarpetas();

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
        carpeta: get(selected, 'carpeta', ''),
        ubicacion: get(selected, 'ubicacion', undefined),
      }}
      validationSchema={Yup.object().shape({
        nombre: Yup.string().required(empty),
        descripcion: Yup.string(),
        carpeta: Yup.number().required(empty),
        ubicacion: Yup.mixed(),
      })}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          setSubmitting(true);
          await dispatch(archivosActions.send({ 
            ...values, 
            id: get(selected, 'id', null) 
          })
          ).then(() => {
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
            {console.log(values)}
            <Col sm="12">
              <h4>Datos Principales</h4>
              <FormGroup>
                <Label for="ubicacion">Seleccionar archivo</Label>
                <input  
                  type="file" 
                  name="ubicacion" 
                  id="ubicacion"
                  // component={ImportFileDropzone}
                  onChange={(event) => {setFieldValue("ubicacion", event.currentTarget.files[0])}}
                  className={`form-control ${errors.ubicacion && touched.ubicacion && 'is-invalid'}`} />      
                {errors.ubicacion && touched.ubicacion ? <div className="invalid-feedback">{errors.ubicacion}</div> : null}
              </FormGroup>
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
                <Label for="carpeta">Colocar en carpeta</Label>
                <Field component="select" name="carpeta" id="carpeta" className={`form-control ${errors.carpeta && touched.carpeta && 'is-invalid'}`}>
                  <option defaultValue=""> --- </option>
                  {carpetas.map((carpeta, i) => {
                    return <option key={i} value={carpeta.id}>{carpeta.nombre}</option>
                  })}
                </Field>
                {errors.carpeta && touched.carpeta ? <div className="invalid-feedback">{errors.carpeta}</div> : null}
              </FormGroup>                   
            </Col>
            <pre>

            </pre>

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
