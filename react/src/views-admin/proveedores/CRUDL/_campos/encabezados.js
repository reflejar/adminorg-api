import React from 'react';
import { Row } from "reactstrap";

import { usePuntosDeVenta } from '../../../../utility/hooks/dispatchers';

const Encabezado = ({ documento, setDocumento, errors, update, types }) => {
  const [puntos] = usePuntosDeVenta();

  const handleChange = (event) => {
    const { name, value } = event.target;
  
    setDocumento((state) => ({
      ...state,
      [name]: value
    }));
  };

  const handleNestedFieldChange = (field) => (event) => {
    event.persist();
    const { name, value } = event.target;

    setDocumento({
      ...documento,
      [field]: {
        ...documento[field],
        [name]: value
      }
    });
  };
  
  return (
    <Row>
        
        {types && <div className='form-group col-md-2'>
          <label htmlFor='receipt_type'>Tipo:</label>
          <select
              className={`form-control ${errors.receipt && errors.receipt.receipt_type && 'is-invalid'}`}
              name='receipt_type'
              id='receipt_type'
              value={documento.receipt && documento.receipt.receipt_type}
              disabled={documento.receipt.receipt_type === "Orden de Pago" ? true : false}
              onChange={handleNestedFieldChange('receipt')}>
                <option value=''>---</option>

                {types.map((type) => (
                  <option value={type.id} key={type.id}>{type.nombre}</option>
                ))}            
          </select>
          {errors.receipt && errors.receipt.receipt_type && (
            <div className="invalid-feedback">
              {errors.receipt.receipt_type}
            </div>
          )}

        </div>}

        <div className='form-group col-md-2'>
          <label htmlFor='point_of_sales'>P. VTA: </label>
            {
              documento.receipt.receipt_type === "Orden de Pago" ?
                <select
                  className={`form-control ${errors.receipt && errors.receipt.point_of_sales && 'is-invalid'}`}
                  name='point_of_sales'
                  id='point_of_sales'
                  value={documento.receipt && documento.receipt.point_of_sales}
                  disabled={update ? true : false}
                  onChange={handleNestedFieldChange('receipt')}>
                    <option value=''>---</option>
        
                    {puntos.map((punto) => (
                      <option value={punto.number} key={punto.number}>{punto.number}</option>
                    ))}
                </select> :
                <input
                  type='text'
                  className={`form-control d-block ${errors.receipt && errors.receipt.point_of_sales && 'is-invalid'}`}
                  name='point_of_sales'
                  id='point_of_sales'
                  pattern="[0-9]*"
                  value={documento.receipt.point_of_sales}
                  maxLength={4}
                  onChange={handleNestedFieldChange('receipt')} />
            }          
        </div>          


          
          {errors.receipt && errors.receipt.point_of_sales && (
            <div className="invalid-feedback">
              {errors.receipt.point_of_sales}
            </div>
          )}

        
        <div className='form-group col-md-2'>
          <label htmlFor='receipt_number'>N°:</label>

          <input
            type='text'
            className={`form-control d-block ${errors.receipt && errors.receipt.receipt_number && 'is-invalid'}`}
            name='receipt_number'
            id='receipt_number'
            pattern="[0-9]*"
            mask="0000"
            maxLength={8}
            disabled={documento.receipt.receipt_type === "Orden de Pago" ? true : false}
            value={documento.receipt.receipt_number}
            onChange={handleNestedFieldChange('receipt')} />


          {errors.receipt && errors.receipt.receipt_number && (
            <div className="invalid-feedback">
              {errors.receipt.receipt_number}
            </div>
          )}            
        </div>        


        <div className='form-group col-md-2'>
          <label htmlFor='issued_date'>F. Documento:</label>

          <input
            type='date'
            className={`form-control d-block ${errors.receipt && errors.receipt.issued_date && 'is-invalid'}`}
            name='issued_date'
            id='issued_date'
            disabled={documento.receipt.receipt_type === "Orden de Pago" ? (update?true:false) : false}
            value={documento.receipt.issued_date}
            onChange={handleNestedFieldChange('receipt')} />


          {errors.receipt && errors.receipt.issued_date && (
            <div className="invalid-feedback">
              {errors.receipt.issued_date}
            </div>
          )}            
        </div>

        <div className='form-group col-md-2'>
          <label htmlFor='fecha_operacion'>F. Operación:</label>

          <input
            type='date'
            className='form-control d-block'
            name='fecha_operacion'
            id='fecha_operacion'
            value={documento.fecha_operacion}
            onChange={handleChange} />
        </div>


    </Row>
      

  );
};

export default Encabezado;