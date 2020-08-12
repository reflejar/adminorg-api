import React from 'react';
import { Row, Col } from "reactstrap";
import Switch from "../../../../components/switch/switch"

const Contado = ({ documento, setDocumento }) => {

  const handleChange = () => {

    setDocumento((state) => ({
      ...state,
      contado: !documento.contado
    }));
  };


  return (
    <Row>
      <Col sm="12 text-right">
        <Switch 
          label={"Pagado de contado"}
          action={handleChange}
        />
      </Col>
    </Row>
  );
};

export default Contado;