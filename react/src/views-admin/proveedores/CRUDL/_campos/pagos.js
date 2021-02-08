import React, { useState, useEffect, useCallback } from 'react';
import { Row, Col } from "reactstrap";

// Components
import Spinner from '../../../../components/spinner/spinner';
import { useDeudas } from '../../../../utility/hooks/dispatchers';
import { DebitosTable } from "./tables/debitos";


const filterCompletedObject = (arr) =>
  arr.filter(d => d.checked).map((deuda) => ({
    ...deuda,
    detalle: deuda.detalle,
    monto: deuda.monto,
  }))


const HandlePagos = ({ documento, setDocumento, deudas, errors, update }) => {
  
  const getDeudas = useCallback(() => {
    // let data = [];
    let data_nuevas = [];
    let data_pagadas = [];
    // if (!update) {
      data_nuevas = deudas.map((deuda) => ({
        vinculo: deuda.id,
        documento: `${deuda.documento.receipt.receipt_type} ${deuda.documento.receipt.formatted_number}`,
        detalle: '',
        monto: deuda.saldo,
        max: deuda.saldo,
        checked: false
      }))
    // } else {
      if (documento && documento.pagos) {
        // console.log(documento.pagos)
        data_pagadas = documento.pagos.map((pago) => {
          if (pago.origen) {
            return {
              ...pago,
              documento: `${pago.origen.documento.receipt.receipt_type} ${pago.origen.documento.receipt.formatted_number}`,
              checked: true
            }
          }
          else return {}
        })
      }
    // }
    const data = [...data_pagadas, ...data_nuevas];
    return data 
  }, [deudas, documento]);
  
  const [selectedDeudas, setSelectedDeudas] = useState(getDeudas());

  
  const handleDebitosTableRowSelect = (index) => {
    let updatedDeudas = [...selectedDeudas];
    updatedDeudas[index].checked = !updatedDeudas[index].checked;
    setSelectedDeudas(updatedDeudas);
  };
  
  
  const handleInputTableChange = (event, index) => {
    let updatedDeudas = [...selectedDeudas];
      
    const name = event.target.name;
    const value = event.target.value;
    const deuda = updatedDeudas[index];
    updatedDeudas[index] = { ...deuda, [name]: value };
    
    setSelectedDeudas(updatedDeudas);

  }; 

  useEffect(() => {
    const updatedDeudas = filterCompletedObject(selectedDeudas);
    setDocumento((state) => ({
      ...state,
      pagos: updatedDeudas
    }));
  }, [selectedDeudas, setDocumento])

  return (
    <Row>
      <Col sm="12">
        <h3 className="pl-0 credito__row__header__text">
          {documento.id ? 'Items pagados' : "Items pendientes de pago"}
        </h3>
          {
            selectedDeudas.length > 0 ? 
              <DebitosTable
                errors={errors && errors.pagos}
                update={update}
                dataTable={selectedDeudas.map((deuda) => ({
                  ...deuda,
                  onRowSelect: handleDebitosTableRowSelect,
                  onInputChange: handleInputTableChange,
              }))}/> :
              <p className="red">--- No existen deudas ---</p>
            }
      </Col>
    </Row>
  );
};


const Pagos = ({ documento, setDocumento, destinatario, errors, update }) => {
  const [deudas, loadingDeudas] = useDeudas(false, destinatario);

  return (
    <Row>
      <Col sm="12">
        {loadingDeudas ?
          <div className="loading-modal">
            <Spinner />
          </div>
          :
          <HandlePagos
            documento={documento} 
            setDocumento={setDocumento}
            deudas={deudas}
            errors={errors} 
            update={update}/>
          }
      </Col>
    </Row>
  );
};


export default Pagos;

