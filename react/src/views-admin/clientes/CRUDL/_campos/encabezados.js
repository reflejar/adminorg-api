import React from 'react';
import { Row } from "reactstrap";

import { usePuntosDeVenta } from '../../../../utility/hooks/dispatchers';

const Encabezado = ({ documento, setDocumento, errors, onlyRead, types }) => {
  const [puntos] = usePuntosDeVenta();

  const handleChange = (event) => {
    const { name, value } = event.target;

    if (name === 'condonacion') {
      return setDocumento((state) => ({
        ...state,
        condonacion: !documento.condonacion
      }));
    }    

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
              disabled={onlyRead ? true : (documento.receipt.receipt_type === "Recibo X" ? true : false)}
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
            onlyRead ? <input
                        type='text'
                        className='form-control d-block'
                        name='point_of_sales'
                        id='point_of_sales'
                        value={documento.receipt.point_of_sales}
                        disabled={true} />
                      : <select
                      className={`form-control ${errors.receipt && errors.receipt.point_of_sales && 'is-invalid'}`}
                      name='point_of_sales'
                      id='point_of_sales'
                      value={documento.receipt && documento.receipt.point_of_sales}
                      onChange={handleNestedFieldChange('receipt')}
                      disabled={onlyRead}>
                        <option value=''>---</option>
            
                        {puntos.map((punto) => (
                          <option value={punto.number} key={punto.number}>{punto.number}</option>
                        ))}
                    </select>
          }
          

          {errors.receipt && errors.receipt.point_of_sales && (
            <div className="invalid-feedback">
              {errors.receipt.point_of_sales[0]}
            </div>
          )}
        </div>

        <div className='form-group col-md-2'>
          <label htmlFor='receipt_number'>N°:</label>

          <input
            type='text'
            className='form-control d-block'
            name='receipt_number'
            id='receipt_number'
            value={documento.receipt.receipt_number}
            disabled={true} />
        </div>

        <div className='form-group col-md-2'>
          <label htmlFor='issued_date'>F. Documento:</label>

          <input
            type='date'
            className={`form-control d-block ${errors.receipt && errors.receipt.issued_date && 'is-invalid'}`}
            name='issued_date'
            id='issued_date'
            value={documento.receipt.issued_date}
            disabled={onlyRead}
            onChange={handleNestedFieldChange('receipt')} />


          {errors.receipt && errors.receipt.issued_date && (
            <div className="invalid-feedback">
              {errors.receipt.issued_date[0]}
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
            disabled={onlyRead}
            onChange={handleChange} />
        </div>

        {documento["condonacion"] !== undefined && <div className='form-group mt-4 pl-2  col-md-2'>
          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              name="condonacion"
              checked={documento.condonacion}
              value={documento.condonacion}
              onChange={handleChange}
              disabled={onlyRead}
              id="condonacion"
            />

            <label className="form-check-label" htmlFor="condonacion">
              Sin intereses
            </label>
          </div>
        </div>}

    </Row>
      

  );
};

export default Encabezado;