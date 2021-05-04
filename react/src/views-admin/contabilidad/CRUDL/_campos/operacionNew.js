import React, { useState, useEffect } from 'react';
import { Row, Col } from "reactstrap";
import get from 'lodash/get';

// Components
import Spinner from '../../../../components/spinner/spinner';

import { AppendableRowField } from '../../../../components/form/AppendableRowField';
import { mapToOptions } from '../../../../utility/mappers';

import { useTitulos } from '../../../../utility/hooks/dispatchers';
import { useAppendableField } from '../../../../components/form/hooks';


const filterCompletedObject = (arr, campo) =>
  arr.filter((x) => (x.cuenta && get(x, campo, null) > 0)).map(x => ({...x, monto: get(x, campo, null)}));

const clenaOp = (documento) => {
  // docum.map(op => ({...op, debe:op.monto, haber:op.monto}))
  let operaciones = []
  documento.debe && documento.debe.forEach(op => {operaciones.push({...op, debe:op.monto, haber:undefined})})
  documento.haber && documento.haber.forEach(op => {operaciones.push({...op, debe:undefined, haber:op.monto})})
  return operaciones
  
} 

const OperacionNew = ({ documento, setDocumento, errors, update }) => {
  const [titulos, loadingTitulos] = useTitulos();
  const [cuentas, setCuentas] = useState([])


  useEffect(() => {
    if (!loadingTitulos) {
      let listCuentas = [];
      titulos.filter(t => t.cuentas.length > 0).forEach(t => t.cuentas.forEach(c => {
        listCuentas.push({...c, full_name: c.nombre})
      }));
      setCuentas(listCuentas.sort((a, b) => a.full_name.localeCompare(b.full_name))) 
    }
  }, [loadingTitulos, titulos])

  const cleanItem = {
    debe: undefined,
    haber: undefined,
    detalle: '',
    cuenta: '',
  }


  const [
    operaciones,
    handleOperacionesChange,
    handleOperacionesAppend,
    handleOperacionesPop,
    setOperaciones
  ] = useAppendableField(update ? clenaOp(documento) : [cleanItem, cleanItem], {
    custom: {
      handleChange: (index) => (event) => {
        const name = event.target.name;
        const value = event.target.value;
        const operacion = operaciones[index];
        const updatedOperacion = { ...operacion, [name]: value };

        setOperaciones(index, updatedOperacion);


      }
    },
    cleanItem
  });
  
  useEffect(() => {
    const updatedDebe = filterCompletedObject(operaciones, 'debe');
    const updatedHaber = filterCompletedObject(operaciones, 'haber');
    setDocumento((state) => ({
      ...state,
      debe: updatedDebe,
      haber: updatedHaber,
    }));
  }, [operaciones, setDocumento])


  return (
    <Row>
      <Col sm="12">
        {loadingTitulos ?
            <div className="loading-modal">
              <Spinner />
            </div>
            :        
        <AppendableRowField
          onAppendClick={handleOperacionesAppend}
          onPopClick={handleOperacionesPop}
          data={operaciones}
          errors={errors && errors.operaciones}
          fields={[
          {
            type: 'select',
            name: 'cuenta',
            placeholder: 'Cuenta',
            header: 'Cuenta',
            handleChange: handleOperacionesChange,
            options: (
              <>
                <option value=""> --- </option>
                {mapToOptions(cuentas).map((cuenta) => (
                  <option key={cuenta.value} value={cuenta.value}>
                    {cuenta.label}
                  </option>
                ))}                
              </>
            ),
          }, {
            type: 'number',
            name: 'debe',
            placeholder: 'Debe',
            min: 1,
            header: 'Debe',
            handleChange: handleOperacionesChange
          }, {
            type: 'number',
            name: 'haber',
            placeholder: 'Haber',
            min: 1,
            header: 'Haber',
            handleChange: handleOperacionesChange
          }, {
            type: 'text',
            name: 'detalle',
            placeholder: 'Detalle',
            header: 'Detalle',
            handleChange: handleOperacionesChange
          }]}
          header={{
            title: "Operaciones",
            appendButton: '+ operacion'
          }}
        />
        }
      </Col>
    </Row>
  );
};


export default OperacionNew;