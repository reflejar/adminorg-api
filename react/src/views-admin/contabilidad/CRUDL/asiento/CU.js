import React, { useCallback } from 'react';
import { connect, useDispatch } from 'react-redux';
import moment from 'moment';
import get from 'lodash/get';
import { toastr } from "react-redux-toastr";

// Components
import Spinner from '../../../../components/spinner/spinner';

import { documentosActions } from '../../../../redux/actions/documentos';
import Encabezado from '../_campos/encabezados';
import Descripcion from '../_campos/descripcion';
import OperacionNew from '../_campos/operacionNew';

import Buttons from '../_campos/buttons';
import { asientosTypes } from '../_options/receipt_types';

// Styles
import './index.scss';

import { cuentasActions } from '../../../../redux/actions/cuentas';
import { useDocumento } from '../hooks';

const Asiento = ({ instancia, update, selected, sendAsiento, deleteAsiento, onClose }) => {
  const dispatch = useDispatch();
  
  const {documento, setDocumento, errors, setErrors, loading, setLoading} = useDocumento(selected, update);
  const errorButton = "La suma del debe debe igualar a la suma del haber";


  const checkCondition = () => {
    let totalDebe = 0;
    let totalHaber = 0;

    if (documento.debe && documento.debe.length > 0) {
      totalDebe = documento.debe.reduce((total, d) => Number(total) + Number(d.monto), 0);
    }

    if (documento.haber && documento.haber.length > 0) {
      totalHaber = documento.haber.reduce((total, h) => Number(total) + Number(h.monto), 0);
    }    

    if (Math.round(totalDebe*100) > 0) {
      return Math.round(totalDebe*100) === Math.round(totalHaber*100);
    }
    return false
  } 

  const updateSituation = useCallback(() => {
    const esTitulo = instancia.hasOwnProperty("supertitulo");
    let query = { destinatario: instancia.id, fecha: moment().format('YYYY-MM-DD') }
    if (esTitulo) {
      query = {...query, titulo:1};
    }
    dispatch(cuentasActions.get(query))    
  }, [dispatch, instancia] );

  
  const handleSubmit = useCallback((event) => {
    event.preventDefault();

    setLoading(true);

    sendAsiento(documento)
      .then(() => {
        toastr.success('¡Listo! Asiento cargado con éxito');
        updateSituation();
        onClose(false);
      })
      .catch((error) => {
        const { data } = error;
        setErrors(data);
      })
      .finally(() => setLoading(false))
  }, [setLoading, sendAsiento, documento, updateSituation, onClose, setErrors]);


  const handleDelete = useCallback(() => {
    setLoading(true);
    deleteAsiento(documento.id)
      .then(response => {
        toastr.success('¡Listo! Asiento eliminado con éxito')
        updateSituation();
        onClose(false);
      })
      .catch((error) => toastr.error(error))
      .finally(() => setLoading(false))
  }, [setLoading, deleteAsiento, documento, updateSituation, onClose]);

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
        update={update}
        types={asientosTypes}/>

      <OperacionNew 
        documento={documento} 
        setDocumento={setDocumento} 
        errors={errors} 
        update={update}/>

      <Descripcion 
        documento={documento} 
        setDocumento={setDocumento}
        update={update}/>

      <Buttons 
        documento={documento}     
        update={update} 
        onClose={onClose}
        required={checkCondition()}
        error={!checkCondition() && errorButton}
        handleDelete={handleDelete} />

    </form>
  );
};

const mapStateToProps = state => ({
  instancia: get(state, 'contabilidad.instance', {}),
})


const mapDispatchToProps = dispatch => ({
  sendAsiento: (payload) => dispatch(documentosActions.send("asiento", payload)),
  deleteAsiento: id => dispatch(documentosActions.remove("asiento", id)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Asiento);