import React from 'react';
import { Row } from "reactstrap";

const Encabezado = ({ documento, setDocumento, onlyRead, types }) => {

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
              className={"form-control"}
              name='receipt_type'
              id='receipt_type'
              value={documento.receipt && documento.receipt.receipt_type}
              disabled={true}
              onChange={handleNestedFieldChange('receipt')}>
                <option value=''>---</option>

                {types.map((type) => (
                  <option value={type.id} key={type.id}>{type.nombre}</option>
                ))}            
          </select>

        </div>}

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
          <label htmlFor='issued_date'>F. Asiento:</label>

          <input
            type='date'
            className={"form-control"}
            name='issued_date'
            id='issued_date'
            value={documento.receipt.issued_date}
            disabled={onlyRead}
            onChange={handleNestedFieldChange('receipt')} />

        </div>

    </Row>
      

  );
};

export default Encabezado;