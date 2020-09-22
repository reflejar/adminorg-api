import React from 'react';
import { Row, Col } from "reactstrap";

const Descripcion = ({ documento, setDocumento, onlyRead }) => {

  const handleChange = (event) => {
    const { name, value } = event.target;

    setDocumento((state) => ({
      ...state,
      [name]: value
    }));
  };


  return (
    <Row>
      <Col sm="12">
          <h3 className="credito__row__header__text mt-2">
            Descripción
          </h3>

          <div className="form-group">
            <textarea
              className="form-control"
              name="descripcion"
              disabled={onlyRead}
              rows={3}
              value={(onlyRead && documento && documento.descripcion) ? documento.descripcion : documento.descripcion}
              onChange={handleChange} />
          </div>
      </Col>
    </Row>
  );
};

export default Descripcion;