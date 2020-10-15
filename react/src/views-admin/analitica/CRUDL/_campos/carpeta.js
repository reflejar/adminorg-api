import React from 'react';
import { Row, Col } from "reactstrap";

import { useCarpetas } from '../../../../utility/hooks/dispatchers';

const Carpeta = ({ archivo, setArchivo }) => {

    const [carpetas] = useCarpetas();

  const handleChange = () => (event) => {
    event.persist();
    const { name, value } = event.target;

    setArchivo((state) => ({
      ...state,
      carpeta: value
    }));
  };


  return (
  
      <Row>
        <Col sm="12">
  
            <div className="form-group">
              <label htmlFor='carpeta'>Colocar en carpeta</label>
                <select
                className={"form-control"}
                name='carpeta'
                id='carpeta'
                value={archivo.carpeta}
                onChange={handleChange()}>
                    <option value=''>---</option>
                    {carpetas.map((carpeta) => (
                    <option value={carpeta.id} key={carpeta.id}>{carpeta.nombre}</option>
                    ))}            
                </select>
            </div>
        </Col>
      </Row>

  );
};

export default Carpeta;