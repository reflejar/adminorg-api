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
import DebitoNew from '../_campos/debitoNew';
import Contado from '../_campos/contado';
import Buttons from '../_campos/buttons';
import { documentosTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { deudasActions } from '../../../../redux/actions/deudas';
import { saldosActions } from '../../../../redux/actions/saldos';
import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const Documento = ({ destinatario, update, selected, sendDocumento, deleteDocumento, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, destinatario, update);

  useEffect(() => {
    if (!documento.debitos) {   
      setDocumento((state) => ({
        ...state,
        contado: false,
        debitos: []
      }))
    }

  }, [documento, setDocumento]);    


  const checkCondition = () => {
    if (documento.debitos && documento.debitos.length > 0) {
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

    sendDocumento(documento)
      .then(() => {
        toastr.success('¡Listo! Documento cargado con éxito');
        updateSituation();
        documento.contado ? onClose("cobrar") : onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendDocumento, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteDocumento(documento.id)
      .then(response => {
        toastr.success('¡Listo! Documento eliminado con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteDocumento, documento, updateSituation, onClose]);

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
        update={update}
        types={documentosTypes}/>

      <DebitoNew 
        documento={documento} 
        setDocumento={setDocumento} 
        errors={errors} 
        update={update}/>

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}
        update={update}/>

      {!update && 
        <Contado 
        documento={documento}     
        setDocumento={setDocumento}/>
      }
      
      <Buttons 
        documento={documento}     
        update={update} 
        onClose={onClose}
        required={checkCondition()} 
        error={null}
        handleDelete={handleDelete}/>

    </form>
  );
};

const mapStateToProps = state => ({
  destinatario: get(state, 'proveedores.instance', {}),
})

const mapDispatchToProps = dispatch => ({
  sendDocumento: (payload) => dispatch(documentosActions.send("proveedor", payload)),
  deleteDocumento: id => dispatch(documentosActions.remove("proveedor", id)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Documento);