import React from 'react';
import { Row, Col } from "reactstrap";
import { ImportFileDropzone } from '../../../../components/dropzone/ImportFileDropzone';

const Ubicacion = ({ archivo, setArchivo }) => {

  const handleChange = (field) => (event) => {
    event.persist();
    const { name, value } = event.target;

    setArchivo((state) => ({
      ...state,
      [name]: value
    }));
  };

  const handleDrop = (files) => {
    // Cleaning previous errors
    console.log("hola")
  }

  return (

    <Row>
        <Col sm="12">
          <div className="ImportFileDropzone__container">
            <ImportFileDropzone accept={['text/csv', 
            ".pdf", 
            ".doc", 
            ".docx", 
            ".xls", 
            ".xlsx"
            ]} onDrop={handleDrop} />
          </div>
        </Col>
    </Row>


  );
};

export default Ubicacion;