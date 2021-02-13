import React, { useState, useEffect, useCallback } from 'react';
import { Row, Col } from "reactstrap";

// Components

import { RetencionesTable } from "./tables/retenciones";

const filterCompletedObject = (arr) =>
  arr.filter(d => d.checked).map((retencion) => ({
    ...retencion,
    detalle: retencion.detalle,
    monto: retencion.monto,
  }))


const Retenciones = ({ documento, setDocumento, retenciones, errors, update }) => {

  const getRetenciones = useCallback(() => {
    let data = [];
    if (!update) {
      data = retenciones.filter(d => documento.destinatario !== d.cuenta_set[0]).map((retencion) => ({
        retencion: retencion.id,
        detalle: '',
        tipo: retencion.nombre,
        monto: undefined,
        checked: false
      }))
    } else {
      if (documento && documento.retenciones) {
        data = documento.retenciones.map((retencion) => ({
          ...retencion,
          tipo: retencion.retencion.nombre,
          checked: true
        }))
      }
    }
    return data
  }, [update, retenciones, documento]);

  const [selectedRetenciones, setSelectedRetenciones] = useState(getRetenciones());


  
  const handleRetencionesTableRowSelect = (index) => {
    let updatedRetenciones = [...selectedRetenciones];
    updatedRetenciones[index].checked = !updatedRetenciones[index].checked;
    setSelectedRetenciones(updatedRetenciones);

  };
  
  
  const handleMontoTableChange = (event, index) => {
    
    let updatedRetenciones = [...selectedRetenciones];
    updatedRetenciones[index].monto = event.target.value;
    setSelectedRetenciones(updatedRetenciones);

  }; 

  useEffect(() => {
    const updatedRetenciones = filterCompletedObject(selectedRetenciones);
    setDocumento((state) => ({
      ...state,
      retenciones: updatedRetenciones
    }));
  }, [selectedRetenciones, setDocumento])  



  return (
    <Row>
      <Col sm="12">
        {selectedRetenciones.length > 0 ? 
          <RetencionesTable
            documento={documento}
            errors={errors}
            update={update}
            dataTable={selectedRetenciones.map((retencion) => ({
              ...retencion,
              onRowSelect: handleRetencionesTableRowSelect,
              onInputChange: handleMontoTableChange,
          }))}/> :
          <p className="red">--- No existen retenciones ---</p>
          
        }
          

      </Col>
    </Row>
  );
};


export default Retenciones;