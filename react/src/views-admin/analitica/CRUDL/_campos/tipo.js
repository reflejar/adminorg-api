import React, { useEffect } from 'react';
import { Row, Col, FormGroup } from "reactstrap";
import { tiposReporte } from '../_options/tipos_reporte';

const Tipo = ({ filtro, setFiltro }) => {


  const handleChange = () => (event) => {
    event.persist();
    const { value } = event.target;

    setFiltro({
      ...filtro,
      tipo: value
    });
  };
  

  return (
    <Row>
      <Col sm={{size: 3, offset: 9}}>
      <FormGroup>
        <select
            className="form-control"
            name='tipo'
            id='tipo'
            value={filtro.tipo}
            onChange={handleChange()}>
            {tiposReporte.map((tipo) => (
              <option value={tipo.id} key={tipo.id}>{tipo.full_name}</option>
            ))}            
        </select>        
        </FormGroup>
       
      </Col>
    </Row>
  );
};


export default Tipo;