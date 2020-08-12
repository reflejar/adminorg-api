import React, { useState, useEffect, useCallback } from 'react';
import { Row, Col } from "reactstrap";

// Components

import { DisponibilidadesTable } from "./tables/disponibilidades";

const filterCompletedObject = (arr) =>
  arr.filter(d => d.checked).map((saldo) => ({
    ...saldo,
    detalle: saldo.detalle,
    monto: saldo.monto,
  }))



const UtilizacionesDisponibilidades = ({ documento, setDocumento, disponibilidades, errors, onlyRead }) => {

  const getSaldos = useCallback(() => {
    let data = [];
    if (!onlyRead) {
      data = disponibilidades.filter((x) => (x.documento.receipt.receipt_type !== documento.receipt.receipt_type)).map((disponibilidad) => ({
        vinculo: disponibilidad.id,
        detalle: "",
        documento: `${disponibilidad.documento.receipt.receipt_type} - ${disponibilidad.documento.receipt.formatted_number}`,
        monto: disponibilidad.monto,
        max: disponibilidad.monto,
        checked: false
      }))
    } else {
      if (documento && documento.utilizaciones_disponibilidades) {
        data = documento.utilizaciones_disponibilidades.map(utilizacion_disponibilidad => ({
          ...utilizacion_disponibilidad,
          documento: `${utilizacion_disponibilidad.origen.documento.receipt.receipt_type} ${utilizacion_disponibilidad.origen.documento.receipt.formatted_number}`,
          max: utilizacion_disponibilidad.monto,
          checked: true
        }))
      }
    }
    return data
  }, [onlyRead, disponibilidades, documento]);

  const [selectedDisponibilidades, setSelectedDisponibilidades] = useState(getSaldos());  

  
  const handleDisponibilidadesTableRowSelect = (index) => {
    let updatedDisponibilidades = [...selectedDisponibilidades];
    updatedDisponibilidades[index].checked = !updatedDisponibilidades[index].checked;
    setSelectedDisponibilidades(updatedDisponibilidades);
 
  };
  
  
  const handleMontoTableChange = (event, index) => {
    let updatedDisponibilidades = [...selectedDisponibilidades];

          
    const name = event.target.name;
    const value = event.target.value;
    const dispo = updatedDisponibilidades[index];
    updatedDisponibilidades[index] = { ...dispo, [name]: value };

    setSelectedDisponibilidades(updatedDisponibilidades);  

  }; 

  useEffect(() => {
    const updatedDisponibilidades = filterCompletedObject(selectedDisponibilidades);
    setDocumento((state) => ({
      ...state,
      utilizaciones_disponibilidades: updatedDisponibilidades
    }));
  }, [selectedDisponibilidades, setDocumento])  


  return (
    <Row>
      <Col sm="12">
        {selectedDisponibilidades.length > 0 ? 
          <DisponibilidadesTable
            errors={errors}
            onlyRead={onlyRead}
            dataTable={selectedDisponibilidades.map((disponibilidad) => ({
              ...disponibilidad,
              onRowSelect: handleDisponibilidadesTableRowSelect,
              onInputChange: handleMontoTableChange,
          }))}/> :
          <p className="red">--- No existen disponibilidades ---</p>
          
        }
          

      </Col>
    </Row>
  );
};


export default UtilizacionesDisponibilidades;