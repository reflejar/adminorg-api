import React, { useEffect, useState } from 'react';
import { Row, Col, Tooltip } from 'reactstrap';

const Buttons = ({ item, update, onClose, required, error, handleDelete }) => {
  
  const [tooltipOpen, setTooltipOpen] = useState(false);
  const [isDisabled, setIsDisabled] = useState(true);
  
  const toggle = () => setTooltipOpen(!tooltipOpen);

  useEffect(() => {   
    if (
      required
      ){
      setIsDisabled(false);
    } else {
      setIsDisabled(true);
    }
  }, [item, required]);        

  return (
    <Row>
      <Col sm="12">
        <div className='text-right'>
          <button type='button' className='btn btn-secondary mr-2' onClick={() => {onClose(false)}}>
            Cancelar
          </button>

          {update && (
            <button
              type='button'
              className='btn btn-danger mr-2'
              onClick={() => { if (window.confirm('Esta seguro que desea eliminar esto?')) handleDelete() } }
            >
              Eliminar
            </button>
          )}      

          <button
            type='submit'
            className='btn btn-primary'
            id="submit-button"
            disabled={update || isDisabled}>
            Consultar
          </button>
          
        </div>
  
          {error && (
            <Tooltip placement="right" isOpen={tooltipOpen} target="submit-button" toggle={toggle}>
              {error}
            </Tooltip> 
          )}

      </Col>
    </Row>
  );
};

export default Buttons;