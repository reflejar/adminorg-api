import React, { useState, useEffect } from 'react';
import moment from 'moment';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';
import { usePlataformas } from '../../../../utility/hooks/dispatchers';
import { PlataformaTable } from "./tables/plataforma";


const UtilizacionPlataforma = ({ documento, setDocumento, destinatario, errors, onlyRead }) => {
  const [plataformas, loadingPlataforma] = usePlataformas(documento.fecha_operacion);

  
  const handlePlataformaTableRowSelect = (index) => {

    setDocumento((state) => ({
      ...state,
      utilizacion_plataforma: index
    }));    
  };
  
  const listPlataforma = () => {
    if (onlyRead && documento.utilizacion_plataforma) {
      return documento.utilizacion_plataforma; 
    }
    return plataformas;
  }


  if (loadingPlataforma) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <Row>
      <Col sm="12">
        {listPlataforma().length > 0 ? 
          <PlataformaTable
            errors={errors}
            onlyRead={onlyRead}
            dataTable={listPlataforma().map((plataforma) => ({
              ...plataforma,
              onRowSelect: handlePlataformaTableRowSelect,
          }))}/> :
          <p className="red">--- No existen pagos desde plataforma ---</p>
          
        }
          

      </Col>
    </Row>
  );
};


export default UtilizacionPlataforma;