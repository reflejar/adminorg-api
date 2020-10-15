import React, {Fragment} from 'react';
import { Row, Col } from "reactstrap";

const Basico = ({ archivo, setArchivo, update }) => {

  const handleNestedFieldChange = (field) => (event) => {
    event.persist();
    const { name, value } = event.target;

    setArchivo((state) => ({
      ...state,
      [name]: value
    }));
  };


  return (
    <Fragment>
      <Row>
        <Col sm="12">
            <div className='form-group'>
              <label htmlFor='nombre'>Nombre</label>
              <input
                type='text'
                className='form-control d-block'
                name='nombre'
                id='nombre'
                value={(update && archivo && archivo.nombre) ? archivo.nombre : archivo.nombre}
                onChange={handleNestedFieldChange('nombre')}
                />
            </div>
        </Col>
      </Row>
  
      <Row>
        <Col sm="12">
  
            <div className="form-group">
              <label htmlFor='descripcion'>Descripcion</label>
              <textarea
                className="form-control"
                name="descripcion"
                rows={3}
                value={(update && archivo && archivo.descripcion) ? archivo.descripcion : archivo.descripcion}
                onChange={handleNestedFieldChange('descripcion')}
                // onChange={handleChange} 
                />
            </div>
        </Col>
      </Row>
        
    </Fragment>

  );
};

export default Basico;