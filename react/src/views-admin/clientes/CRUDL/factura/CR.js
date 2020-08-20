import React, { useCallback, useEffect } from 'react';
import { connect, useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';
import { toastr } from "react-redux-toastr";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { documentosActions } from '../../../../redux/actions/documentos';
import Encabezado from '../_campos/encabezados';
import Descripcion from '../_campos/descripcion';
import CreditoNew from '../_campos/creditoNew';
import Contado from '../_campos/contado';
import Buttons from '../_campos/buttons';
import { facturasTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const Comprobante = ({ destinatario, onlyRead, selected, sendComprobante, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, onlyRead);

  useEffect(() => {
    if (!documento.creditos) {   
      setDocumento((state) => ({
        ...state,
        contado: false,
        creditos: []
      }))
    }

  }, [documento, setDocumento]);    


  const checkCondition = () => {
    if (documento.creditos && documento.creditos.length > 0) {
      return true;
    }
    return false;
  } 

  const updateSituation = useCallback(() => {
    dispatch(deudasActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD'), capture: true }));
    dispatch(saldosActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD'), capture: true }));
    dispatch(cuentasActions.get({ destinatario: destinatario.id, fecha: moment().format('YYYY-MM-DD') }));
  }, [dispatch, destinatario] );

  

  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    setLoading(true);
    
    sendComprobante(documento)
      .then(() => {
        toastr.success('¡Listo! Comprobante cargada con éxito');
        updateSituation();
        documento.contado ? onClose("cobrar") : onClose(false);        
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendComprobante, documento, updateSituation, onClose, setErrors]);

  if (loading) {
    return (
      <div className='loading-modal'>
        <Spinner />
      </div>
    )
  }

  return (
    <form className='credito-invoice container' onSubmit={handleSubmit}>
      <Encabezado 
        documento={documento} 
        setDocumento={setDocumento} 
        errors={errors} 
        onlyRead={onlyRead}
        types={facturasTypes}/>

      <CreditoNew 
        documento={documento} 
        setDocumento={setDocumento} 
        destinatario={destinatario} 
        errors={errors} 
        onlyRead={onlyRead}/>

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}
        onlyRead={onlyRead}/>

      {!onlyRead && 
        <Contado 
        documento={documento}     
        setDocumento={setDocumento}
        onlyRead={onlyRead} />
      }
      
      <Buttons 
        documento={documento}     
        onlyRead={onlyRead} 
        onClose={onClose}
        required={checkCondition()} />

    </form>
  );
};

const mapStateToProps = state => ({
  destinatario: get(state, 'clientes.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendComprobante: (payload) => dispatch(documentosActions.send("cliente", payload))
});

export default connect(mapStateToProps, mapDispatchToProps)(Comprobante);