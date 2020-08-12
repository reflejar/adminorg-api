import React, { useState, useEffect, useCallback } from 'react';
import { Row, Col } from "reactstrap";

// Components

import { SaldosTable } from "./tables/saldos";

const filterCompletedObject = (arr, cobros) =>
  arr.filter((d => d.checked && cobros && cobros.length > 0)).map((saldo) => ({
    ...saldo,
    detalle: saldo.detalle,
    monto: saldo.monto,
  }))


const UtilizacionesSaldos = ({ documento, setDocumento, saldos, errors, onlyRead }) => {

  const getSaldos = useCallback(() => {
    let data = [];
    if (!onlyRead) {
      data = saldos.map((saldo) => ({
        vinculo: saldo.id,
        documento: `${saldo.documento.receipt.receipt_type} ${saldo.documento.receipt.formatted_number}`,
        detalle: '',
        monto: saldo.saldo,
        max: saldo.saldo,
        checked: false
      }))
    } else {
      if (documento && documento.utilizaciones_saldos) {
        data = documento.utilizaciones_saldos.map(utilizacion_saldo => ({
          ...utilizacion_saldo,
          documento: `${utilizacion_saldo.origen.documento.receipt.receipt_type} ${utilizacion_saldo.origen.documento.receipt.formatted_number}`,
          max: utilizacion_saldo.monto,
          checked: true
        }))
      }
    }
    return data
  }, [onlyRead, saldos, documento]);

  const [selectedSaldos, setSelectedSaldos] = useState(getSaldos());  
  
  
  const handleSaldosTableRowSelect = (index) => {
    let updatedSaldos = [...selectedSaldos];
    updatedSaldos[index].checked = !updatedSaldos[index].checked;
    setSelectedSaldos(updatedSaldos);

  };
  
  
  const handleInputTableChange = (event, index) => {
    let updatedSaldos = [...selectedSaldos];

          
    const name = event.target.name;
    const value = event.target.value;
    const deuda = updatedSaldos[index];
    updatedSaldos[index] = { ...deuda, [name]: value };

    setSelectedSaldos(updatedSaldos);    

  }; 

  useEffect(() => {
    const updatedSaldos = filterCompletedObject(selectedSaldos, documento.cobros);
    setDocumento((state) => ({
      ...state,
      utilizaciones_saldos: updatedSaldos
    }));
  }, [selectedSaldos, documento.cobros, setDocumento])  


  return (
    <Row>
      <Col sm="12">
        {selectedSaldos.length > 0 ? 
          <SaldosTable
            errors={errors}
            onlyRead={onlyRead}
            dataTable={selectedSaldos.map((saldo) => ({
              ...saldo,
              onRowSelect: handleSaldosTableRowSelect,
              onInputChange: handleInputTableChange,
          }))}/> :
          <p className="red">--- No existen saldos a favor ---</p>
          
        }
          

      </Col>
    </Row>
  );
};


export default UtilizacionesSaldos;