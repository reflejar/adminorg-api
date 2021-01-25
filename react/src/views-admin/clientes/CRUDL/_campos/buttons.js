import React, { useEffect, useState } from 'react';
import { Tooltip } from 'reactstrap';

const Buttons = ({ documento, onlyRead, onClose, required, error, handleDelete }) => {
  
  const [tooltipOpen, setTooltipOpen] = useState(false);
  const [isDisabled, setIsDisabled] = useState(true);
  
  const toggle = () => setTooltipOpen(!tooltipOpen);

  useEffect(() => {   
    if (
      documento.receipt.receipt_type && 
      documento.receipt.point_of_sales && 
      documento.receipt.issued_date && 
      documento.fecha_operacion && 
      required
      ){
      setIsDisabled(false);
    } else {
      setIsDisabled(true);
    }
  }, [documento, required]);        

  return (
      <div className='row'>
        <div className='col-12 text-right'>

          <button type='button' className='btn btn-secondary mr-2' onClick={() => {onClose(false)}}>
            Cancelar
          </button>

          {onlyRead && documento.pdf && (
            <a
              href={documento.pdf}
              type='button'
              className='btn btn-warning mr-2'
              target="_blank"
              rel="noopener noreferrer"
            >
              Imprimir
            </a>
          )}

          {onlyRead && !documento.fecha_anulacion && documento.receipt.receipt_type === "Recibo X" && (
            <button
              type='button'
              className='btn btn-danger mr-2'
              onClick={() => { if (window.confirm('Esta seguro que desea anular este Documento?')) handleDelete() } }
            >
              Anular
            </button>
          )}      


          <button
            type='submit'
            className='btn btn-primary'
            id="submit-button"
            disabled={onlyRead || isDisabled}>
            Guardar
          </button>
  
          {error && (
            <Tooltip placement="right" isOpen={tooltipOpen} target="submit-button" toggle={toggle}>
              {error}
            </Tooltip> 
          )}
        </div>
      </div>
  );
};

export default Buttons;