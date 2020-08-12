import React, { useState, useEffect } from 'react';
import { Row, Col } from "reactstrap";

// Components

import { DisponibilidadesTable } from "./tables/disponibilidades";


const UtilizacionesDisponibilidades = ({ documento, setDocumento, disponibilidades, errors, onlyRead }) => {
  const [selectedDisponibilidades, setSelectedDisponibilidades] = useState([]);


  useEffect(() => {
    if (disponibilidades) {   
      setSelectedDisponibilidades(disponibilidades.map((disponibilidad) => ({
        id: disponibilidad.id,
        detalle: '',
        origen: `${disponibilidad.documento.receipt.receipt_type} - ${disponibilidad.documento.receipt.formatted_number}`,
        monto: disponibilidad.monto,
        max: disponibilidad.monto,
        checked: false
      })))
    }

  }, [disponibilidades, setSelectedDisponibilidades]);   


  
  const handleDisponibilidadesTableRowSelect = (index) => {
    let updatedDisponibilidades = [...selectedDisponibilidades];
    updatedDisponibilidades[index].checked = !updatedDisponibilidades[index].checked;
    setSelectedDisponibilidades(updatedDisponibilidades);

    setDocumento((state) => ({
      ...state,
      utilizaciones_disponibilidades: prepareSelectedUtilizacionesDisponibilidades()
    }));    
  };
  
  
  const handleMontoTableChange = (event, index) => {
    
    let updatedDisponibilidades = [...selectedDisponibilidades];
    updatedDisponibilidades[index].monto = event.target.value;
    setSelectedDisponibilidades(updatedDisponibilidades);

    setDocumento((state) => ({
      ...state,
      utilizaciones_disponibilidades: prepareSelectedUtilizacionesDisponibilidades()
    }));        

  }; 

  const prepareSelectedUtilizacionesDisponibilidades = () => {
    return selectedDisponibilidades.filter(d => d.checked).map((disponibilidad) => ({
      vinculo: disponibilidad.id,
      detalle: disponibilidad.detalle,
      monto: disponibilidad.monto,
  }))
  }

  const listDisponibilidades = () => {
    if (onlyRead && documento.utilizaciones_disponibilidades) {
      return documento.utilizaciones_disponibilidades; 
    }
    return selectedDisponibilidades;
  }


  return (
    <Row>
      <Col sm="12">
        {listDisponibilidades().length > 0 ? 
          <DisponibilidadesTable
            errors={errors}
            onlyRead={onlyRead}
            dataTable={listDisponibilidades().map((disponibilidad) => ({
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